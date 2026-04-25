from __future__ import annotations

import re
from datetime import datetime
from typing import TYPE_CHECKING

from geoalchemy2 import Geometry
from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .spoorkabel_prorail_relation import SpoorkabelProrailRelation
    from .tekening_model import Tekening


class ProrailGil(Base):
    __tablename__ = "prorail_gil"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    tekening_id: Mapped[int] = mapped_column(
        ForeignKey("tekeningen.id"), nullable=False
    )

    geom: Mapped[object] = mapped_column(
        Geometry("MULTILINESTRING", srid=28992), nullable=True
    )

    tekeningnaam: Mapped[str] = mapped_column(String(16), nullable=False)
    tekeningversie: Mapped[str] = mapped_column(String(8), nullable=False)
    gil_nummer: Mapped[int | None] = mapped_column(Integer)
    opmerking: Mapped[str | None] = mapped_column(String(1000))
    plaatsingsdatum: Mapped[datetime | None] = mapped_column(DateTime)
    feature_type: Mapped[str | None] = mapped_column(String(32))
    is_existing: Mapped[bool] = mapped_column(Boolean, default=True)

    tekening: Mapped["Tekening"] = relationship(
        "Tekening", back_populates="prorail_gils"
    )
    spoorkabels: Mapped[list["SpoorkabelProrailRelation"]] = relationship(
        "SpoorkabelProrailRelation", back_populates="prorail_gil"
    )

    @hybrid_property
    def discipline(self) -> str | None:
        """Python-side logic for accessing .discipline"""
        if not self.tekeningnaam:
            return None
        # Matches digits, then one of the 4 codes, then digits
        match = re.search(r"(KS|RD|WB|WV)", self.tekeningnaam)
        return match.group(1) if match else None

    @discipline.expression
    def discipline(cls):
        """Database-side logic for filtering: Tekening.discipline == 'KS'"""
        # This uses the POSIX regex extraction supported by PostgreSQL.
        # If using SQLite, you may need a different function.
        return func.substring(cls.tekeningnaam, r"(KS|RD|WB|WV)")
