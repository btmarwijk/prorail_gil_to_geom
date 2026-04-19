from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .prorail_gil_model import ProrailGil
    from .spoorkabel_versie_relation import SpoorkabelVersieDetail


class SpoorkabelProrailRelation(Base):
    __tablename__ = "spoorkabel_prorail_feature_relation"

    id: Mapped[int] = mapped_column(primary_key=True)

    spoorkabel_id: Mapped[int] = mapped_column(
        ForeignKey("kabel_versie_details.id"), primary_key=True
    )
    prorail_feature_id: Mapped[int] = mapped_column(
        ForeignKey("prorail_gil.id"), primary_key=True
    )

    spoorkabel: Mapped["SpoorkabelVersieDetail"] = relationship(
        "SpoorkabelVersieDetail", back_populates="prorail_relations"
    )
    prorail_gil: Mapped["ProrailGil"] = relationship(
        "ProrailGil", back_populates="spoorkabel_relations"
    )
