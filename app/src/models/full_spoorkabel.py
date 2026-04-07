from __future__ import annotations
from geoalchemy2 import Geometry
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING
from .base import Base

if TYPE_CHECKING:
    from models.spoorkabel_model import Spoorkabel


class FullSpoorkabel(Base):
    __tablename__ = "full_spoorkabel"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    geom: Mapped[object] = mapped_column(Geometry("LINESTRING", srid=28992), nullable=True)

    kabelnaam: Mapped[str | None] = mapped_column(String)
    kabeltype: Mapped[str | None] = mapped_column(String)
    kabelnummer: Mapped[str | None] = mapped_column(String(255))  # String in original schema
    oud_nieuw: Mapped[str | None] = mapped_column(String)
    groep: Mapped[str | None] = mapped_column(String)
    sub_groep: Mapped[str | None] = mapped_column(String)

    spoorkabel: Mapped[list[Spoorkabel]] = relationship(
        "Spoorkabel", back_populates="full_spoorkabel"
    )