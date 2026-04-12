from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .spoorkabel_versie_relation import SpoorkabelVersieDetail

if TYPE_CHECKING:
    from .tekening_model import Tekening


class Versie(Base):
    __tablename__ = "versies"

    id: Mapped[int] = mapped_column(primary_key=True)
    tekening_id: Mapped[int] = mapped_column(
        ForeignKey("tekeningen.id"), nullable=False
    )
    versie: Mapped[str | None] = mapped_column(String)
    discipline: Mapped[str | None] = mapped_column(String)
    download_date: Mapped[datetime | None] = mapped_column(DateTime)
    geocode_naam: Mapped[str] = mapped_column(String(50))
    export_date: Mapped[datetime] = mapped_column(DateTime)

    # Relaties
    tekening: Mapped["Tekening"] = relationship("Tekening", back_populates="versies")
    spoorkabel_details: Mapped[list["SpoorkabelVersieDetail"]] = relationship(
        "SpoorkabelVersieDetail", back_populates="versie"
    )
