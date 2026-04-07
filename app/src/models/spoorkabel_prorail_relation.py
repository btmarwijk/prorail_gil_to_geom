from __future__ import annotations
from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING

from .base import Base

if TYPE_CHECKING:
    from .prorail_gil_model import ProrailGil
    from .spoorkabel_model import Spoorkabel

class SpoorkabelProrailRelation(Base):
    __tablename__ = "spoorkabel_prorail_feature_relation"
 
    spoorkabel_id: Mapped[int] = mapped_column(
        ForeignKey("spoorkabel.id"), primary_key=True
    )
    prorail_feature_id: Mapped[int] = mapped_column(
        ForeignKey("prorail_gil.id"), primary_key=True
    )
 
    # Denormalised payload retained from original schema
    kabelnaam: Mapped[str | None] = mapped_column(String)
    kabeltype: Mapped[str | None] = mapped_column(String)
    kabelnummer: Mapped[int | None] = mapped_column(Integer)
    gil_nummer: Mapped[int | None] = mapped_column(Integer)
    feature_type: Mapped[str | None] = mapped_column(String)
    oud_nieuw: Mapped[str | None] = mapped_column(String)
 
    spoorkabel: Mapped["Spoorkabel"] = relationship(
        "Spoorkabel", back_populates="prorail_relations"
    )
    prorail_gil: Mapped["ProrailGil"] = relationship(
        "ProrailGil", back_populates="spoorkabel_relations"
    )