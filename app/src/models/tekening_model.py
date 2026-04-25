import re
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String, func
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .mixins import TimestampMixin

if TYPE_CHECKING:
    from .location_model import Location
    from .project_model import Project
    from .prorail_gil_model import ProrailGil
    from .upload_model import Upload
    from .versie_model import Versie


class Tekening(TimestampMixin, Base):
    __tablename__ = "tekeningen"

    id: Mapped[int] = mapped_column(primary_key=True)
    upload_id: Mapped[int] = mapped_column(ForeignKey("upload.id"), nullable=False)
    project_id: Mapped[int] = mapped_column(ForeignKey("projecten.id"), nullable=True)
    naam: Mapped[str] = mapped_column(String(100))
    geocodenaam: Mapped[str | None] = mapped_column(String(50))
    regio: Mapped[str | None] = mapped_column(String(64))

    project: Mapped["Project"] = relationship("Project", back_populates="tekeningen")
    upload: Mapped["Upload"] = relationship("Upload", back_populates="tekeningen")
    versies: Mapped[list["Versie"]] = relationship("Versie", back_populates="tekening")
    prorail_gils: Mapped[list["ProrailGil"]] = relationship(
        "ProrailGil", back_populates="tekening"
    )

    location: Mapped["Location"] = relationship("Location", back_populates="tekening")

    @hybrid_property
    def discipline(self) -> str | None:
        """Python-side logic for accessing .discipline"""
        if not self.naam:
            return None
        # Matches digits, then one of the 4 codes, then digits
        match = re.search(r"(KS|RD|WB|WV)", self.naam)
        return match.group(1) if match else None

    @discipline.expression
    def discipline(cls):
        """Database-side logic for filtering: Tekening.discipline == 'KS'"""
        # This uses the POSIX regex extraction supported by PostgreSQL.
        # If using SQLite, you may need a different function.
        return func.substring(cls.naam, r"(KS|RD|WB|WV)")
