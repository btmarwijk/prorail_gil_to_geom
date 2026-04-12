from typing import TYPE_CHECKING

from geoalchemy2 import Geometry
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .spoorkabel_versie_relation import SpoorkabelVersieDetail


class SpoorkabelGeometrie(Base):
    __tablename__ = "spoorkabel_geometrieen"

    id: Mapped[int] = mapped_column(primary_key=True)
    versie_details_id = mapped_column(
        ForeignKey("kabel_versie_details.id"), nullable=False
    )
    geom: Mapped[Geometry] = mapped_column(
        Geometry(geometry_type="MULTILINESTRING", srid=28992)
    )

    geometry_hash: Mapped[int] = mapped_column(String(64), unique=True, index=True)

    versie_details: Mapped[list["SpoorkabelVersieDetail"]] = relationship(
        "SpoorkabelVersieDetail", back_populates="geometrie"
    )
