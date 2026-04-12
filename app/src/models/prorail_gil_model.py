from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from geoalchemy2 import Geometry
from sqlalchemy import DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .spoorkabel_prorail_relation import SpoorkabelProrailRelation


class ProrailGil(Base):
    __tablename__ = "prorail_gil"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    geom: Mapped[object] = mapped_column(
        Geometry("MULTILINESTRING", srid=28992), nullable=True
    )

    tekeningnaam: Mapped[str] = mapped_column(String(16), nullable=False)
    tekeningversie: Mapped[str] = mapped_column(String(8), nullable=False)
    gil_nummer: Mapped[int | None] = mapped_column(Integer)
    opmerking: Mapped[str | None] = mapped_column(String(1000))
    plaatsingsdatum: Mapped[datetime | None] = mapped_column(DateTime)
    feature_type: Mapped[str | None] = mapped_column(String(32))
    discipline: Mapped[str | None] = mapped_column(String)

    spoorkabel_relations: Mapped[list["SpoorkabelProrailRelation"]] = relationship(
        "SpoorkabelProrailRelation", back_populates="prorail_gil"
    )
