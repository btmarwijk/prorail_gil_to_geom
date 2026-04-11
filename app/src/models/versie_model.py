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
    versie_naam: Mapped[str] = mapped_column(String(50))  # Bijv. "X", "Y", "Z"
    export_datum: Mapped[datetime] = mapped_column(DateTime)  # Datum uit de Excel
    upload_datum: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    # Relaties
    tekening: Mapped["Tekening"] = relationship(back_populates="versies")
    spoorkabel_details: Mapped[list["SpoorkabelVersieDetail"]] = relationship(
        back_populates="versie"
    )
