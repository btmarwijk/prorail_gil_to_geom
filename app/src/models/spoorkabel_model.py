from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from geoalchemy2 import Geometry
from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .full_spoorkabel import FullSpoorkabel
    from .spoorkabel_prorail_relation import SpoorkabelProrailRelation
    from .spoorkabel_versie_relation import SpoorkabelVersieDetail


class Spoorkabel(Base):
    __tablename__ = "spoorkabel"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    versie_details_id: Mapped[int] = mapped_column(
        ForeignKey("kabel_versie_details.id"), nullable=False
    )
    full_spoorkabel_id: Mapped[int | None] = mapped_column(
        ForeignKey("full_spoorkabel.id"), nullable=True
    )

    geom: Mapped[object] = mapped_column(
        Geometry("LINESTRING", srid=28992), nullable=True
    )

    kabelnaam: Mapped[str | None] = mapped_column(String)
    kabeltype: Mapped[str | None] = mapped_column(String)
    van: Mapped[str | None] = mapped_column(String)
    naar: Mapped[str | None] = mapped_column(String)
    groep: Mapped[str | None] = mapped_column(String)
    sub_groep: Mapped[str | None] = mapped_column(String)
    oud_nieuw: Mapped[str | None] = mapped_column(String)
    kabel_geboren: Mapped[datetime | None] = mapped_column(DateTime)
    kabelnummer: Mapped[int | None] = mapped_column(Integer)
    opmerking: Mapped[str | None] = mapped_column(Text)
    tekeningnaam: Mapped[str | None] = mapped_column(String)
    created_at: Mapped[datetime | None] = mapped_column(DateTime)

    versie_details: Mapped[SpoorkabelVersieDetail] = relationship(
        "SpoorkabelVersieDetail", back_populates="spoorkabel"
    )
    full_spoorkabel: Mapped["FullSpoorkabel | None"] = relationship(
        "FullSpoorkabel", back_populates="spoorkabel"
    )
    prorail_relations: Mapped[list["SpoorkabelProrailRelation"]] = relationship(
        "SpoorkabelProrailRelation", back_populates="spoorkabel"
    )
