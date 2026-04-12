from typing import TYPE_CHECKING

from geoalchemy2 import Geometry
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .tekening_model import Tekening


class Location(Base):
    # TODO: Add this to Tekening
    __tablename__ = "locations"

    # Primary key
    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    # Dutch administrative divisions
    provincie: Mapped[str] = mapped_column(String(100), nullable=False)
    waterschap: Mapped[str] = mapped_column(String(100), nullable=False)
    gemeente: Mapped[str] = mapped_column(String(100), nullable=False)
    wijk: Mapped[str] = mapped_column(String(100), nullable=False)
    buurt: Mapped[str] = mapped_column(String(100), nullable=False)

    # Geometry - Point in EPSG:28992 (RD New - Dutch coordinate system)
    geometry: Mapped[Geometry] = mapped_column(
        Geometry("POINT", srid=28992), nullable=False
    )

    tekening: Mapped["Tekening"] = relationship("Tekening", back_populates="location")

    def __repr__(self) -> str:
        return (
            f"<Location(id={self.id}, "
            f"provincie={self.provincie}, "
            f"gemeente={self.gemeente}, "
            f"buurt={self.buurt})>"
        )
