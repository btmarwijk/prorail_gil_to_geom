from datetime import datetime
from typing import TYPE_CHECKING, List

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .location_model import Location
    from .project_model import Project
    from .upload_model import Upload
    from .versie_model import Versie


class Tekening(Base):
    __tablename__ = "tekeningen"

    id: Mapped[int] = mapped_column(primary_key=True)
    upload_id: Mapped[int] = mapped_column(ForeignKey("upload.id"), nullable=False)
    project_id: Mapped[int] = mapped_column(ForeignKey("projecten.id"), nullable=False)
    naam: Mapped[str] = mapped_column(String(100))

    bestandnaam: Mapped[str | None] = mapped_column(String)
    processing_time: Mapped[str | None] = mapped_column(String)
    success: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    project: Mapped["Project"] = relationship("Project", back_populates="tekeningen")
    upload: Mapped["Upload"] = relationship("Upload", back_populates="tekeningen")
    versies: Mapped[List["Versie"]] = relationship("Versie", back_populates="tekening")

    location: Mapped["Location"] = relationship("Location", back_populates="tekening")
