from typing import TYPE_CHECKING, Optional

from sqlalchemy import Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .enums.enums import SpoorkabelStatus

if TYPE_CHECKING:
    from .spoorkabel_geometrie import SpoorkabelGeometrie
    from .spoorkabel_model import Spoorkabel
    from .versie_model import Versie


class SpoorkabelVersieDetail(Base):
    """
    De koppeltabel die per versie vastlegt welke kabel welke geometrie gebruikte.
    """

    __tablename__ = "kabel_versie_details"

    id: Mapped[int] = mapped_column(primary_key=True)
    kabel_id: Mapped[int] = mapped_column(ForeignKey("spoorkabel.id"), nullable=False)
    versie_id: Mapped[int] = mapped_column(ForeignKey("versies.id"), nullable=False)

    # De verwijzing naar de unieke geometrie
    geometrie_id: Mapped[int] = mapped_column(
        ForeignKey("spoorkabel_geometrieen.id"), nullable=False
    )

    status: Mapped[SpoorkabelStatus] = mapped_column(Enum(SpoorkabelStatus))
    lengte: Mapped[Optional[float]] = mapped_column()

    # Relaties
    spoorkabel: Mapped["Spoorkabel"] = relationship(
        "Spoorkabel", back_populates="versie_details"
    )
    versie: Mapped["Versie"] = relationship("Versie", back_populates="kabel_details")
    geometrie: Mapped["SpoorkabelGeometrie"] = relationship(
        "SpoorkabelGeometrie", back_populates="versie_details"
    )
