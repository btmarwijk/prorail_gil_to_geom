from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from geoalchemy2 import Geometry
from sqlalchemy import DateTime, Float, Integer, String, Text
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .mixins import TimestampMixin

if TYPE_CHECKING:
    from .spoorkabel_prorail_relation import SpoorkabelProrailRelation
    from .spoorkabel_versie_relation import SpoorkabelVersieDetail


class Spoorkabel(TimestampMixin, Base):
    __tablename__ = "spoorkabel"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    kabelnaam: Mapped[str | None] = mapped_column(String)
    kabelnaam_oud: Mapped[str | None] = mapped_column(String)
    kabeltype: Mapped[str | None] = mapped_column(String)
    van: Mapped[str | None] = mapped_column(String)
    naar: Mapped[str | None] = mapped_column(String)
    groep: Mapped[str | None] = mapped_column(String)
    sub_groep: Mapped[str | None] = mapped_column(String)
    van_gil: Mapped[str | None] = mapped_column(String)
    naar_gil: Mapped[str | None] = mapped_column(String)
    kabel_geboren: Mapped[datetime | None] = mapped_column(DateTime)
    kabelnummer: Mapped[int | None] = mapped_column(Integer, index=True)
    geulen: Mapped[list[int] | None] = mapped_column(ARRAY(Integer))
    geulen_not_found: Mapped[list[int] | None] = mapped_column(ARRAY(Integer))
    opmerking: Mapped[str | None] = mapped_column(Text)
    max_lengte: Mapped[float | None] = mapped_column(Float)
    tb_lengte: Mapped[float | None] = mapped_column(Float)
    ab_lengte: Mapped[float | None] = mapped_column(Float)
    regelnummer: Mapped[float | None] = mapped_column(Float)

    geom: Mapped[Geometry | None] = mapped_column(
        Geometry(geometry_type="MULTILINESTRING", srid=28992)
    )

    geometry_hash: Mapped[int | None] = mapped_column(
        String(64), unique=True, index=True
    )

    versie_details: Mapped[list["SpoorkabelVersieDetail"]] = relationship(
        "SpoorkabelVersieDetail",
        back_populates="spoorkabel",
        foreign_keys="[SpoorkabelVersieDetail.kabel_id]",  # Be explicit here
    )

    prorail_gils: Mapped[list["SpoorkabelProrailRelation"]] = relationship(
        "SpoorkabelProrailRelation", back_populates="spoorkabel"
    )
