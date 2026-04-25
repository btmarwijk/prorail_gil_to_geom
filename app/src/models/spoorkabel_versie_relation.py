from typing import TYPE_CHECKING

from sqlalchemy import Enum, Float, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .enums.enums import SpoorkabelStatus
from .mixins import TimestampMixin

if TYPE_CHECKING:
    from .spoorkabel_model import Spoorkabel
    from .versie_model import Versie


class SpoorkabelVersieDetail(TimestampMixin, Base):
    """
    De koppeltabel die per versie vastlegt welke kabel welke geometrie gebruikte.
    """

    __tablename__ = "kabel_versie_details"

    id: Mapped[int] = mapped_column(primary_key=True)
    kabel_id: Mapped[int] = mapped_column(ForeignKey("spoorkabel.id"), nullable=True)
    versie_id: Mapped[int] = mapped_column(ForeignKey("versies.id"), nullable=False)

    kabelnummer: Mapped[int] = mapped_column(Integer)

    status: Mapped[SpoorkabelStatus] = mapped_column(
        Enum(SpoorkabelStatus), nullable=True
    )
    lengte: Mapped[float | None] = mapped_column(Float)

    # Relaties
    spoorkabel: Mapped["Spoorkabel"] = relationship(
        "Spoorkabel", back_populates="versie_details", foreign_keys=[kabel_id]
    )
    versie: Mapped["Versie"] = relationship(
        "Versie", back_populates="spoorkabel_details"
    )
