from typing import TYPE_CHECKING, Optional

from geoalchemy2 import Geometry
from sqlalchemy import Enum, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .enums.enums import SpoorkabelStatus

if TYPE_CHECKING:
    from .spoorkabel_model import Spoorkabel
    from .spoorkabel_prorail_relation import SpoorkabelProrailRelation
    from .versie_model import Versie


class SpoorkabelVersieDetail(Base):
    """
    De koppeltabel die per versie vastlegt welke kabel welke geometrie gebruikte.
    """

    __tablename__ = "kabel_versie_details"

    id: Mapped[int] = mapped_column(primary_key=True)
    kabel_id: Mapped[int] = mapped_column(ForeignKey("spoorkabel.id"), nullable=False)
    versie_id: Mapped[int] = mapped_column(ForeignKey("versies.id"), nullable=False)

    status: Mapped[SpoorkabelStatus] = mapped_column(Enum(SpoorkabelStatus))
    lengte: Mapped[Optional[float]] = mapped_column()
    geom: Mapped[Geometry] = mapped_column(
        Geometry(geometry_type="MULTILINESTRING", srid=28992)
    )

    geometry_hash: Mapped[int] = mapped_column(String(64), unique=True, index=True)

    # Relaties
    spoorkabel: Mapped["Spoorkabel"] = relationship(
        "Spoorkabel", back_populates="versie_details", foreign_keys=[kabel_id]
    )
    versie: Mapped["Versie"] = relationship(
        "Versie", back_populates="spoorkabel_details"
    )

    prorail_relations: Mapped[list["SpoorkabelProrailRelation"]] = relationship(
        "SpoorkabelProrailRelation", back_populates="spoorkabel"
    )
