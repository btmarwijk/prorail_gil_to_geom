from __future__ import annotations
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING
from .base import Base

if TYPE_CHECKING:
    from .spoorkabel_model import Spoorkabel
    from .upload_model import Upload

class MetaSpoorkabel(Base):
    __tablename__ = "meta_spoorkabel"
 
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    upload_id: Mapped[int | None] = mapped_column(ForeignKey("upload.id"), nullable=True)
 
    kabelnaam: Mapped[str | None] = mapped_column(String)
    kabeltype: Mapped[str | None] = mapped_column(String)
    tekeningnaam: Mapped[str] = mapped_column(String(255), nullable=False)
    versie: Mapped[str | None] = mapped_column(String)
    geocodenaam: Mapped[str | None] = mapped_column(String)
    oud_nieuw: Mapped[str | None] = mapped_column(String)
    kabelnummer: Mapped[int | None] = mapped_column(Integer)
    kabel_geboren: Mapped[datetime | None] = mapped_column(DateTime)
    kabelnaam_oud: Mapped[str | None] = mapped_column(String)
    van: Mapped[str | None] = mapped_column(String)
    naar: Mapped[str | None] = mapped_column(String)
    discipline: Mapped[str | None] = mapped_column(String)
    groep: Mapped[str | None] = mapped_column(String)
    sub_groep: Mapped[str | None] = mapped_column(String)
    van_gil: Mapped[str | None] = mapped_column(String)
    naar_gil: Mapped[str | None] = mapped_column(String)
    opmerking: Mapped[str | None] = mapped_column(Text)
    geulen: Mapped[str | None] = mapped_column(String(2000))
    max_lengte: Mapped[int | None] = mapped_column(Integer)
    tb_lengte: Mapped[int | None] = mapped_column(Integer)
    ab_lengte: Mapped[int | None] = mapped_column(Integer)
    regelnummer: Mapped[int | None] = mapped_column(Integer)
    gedownload: Mapped[datetime | None] = mapped_column(DateTime)
    created_at: Mapped[datetime | None] = mapped_column(DateTime)
 
    upload: Mapped["Upload | None"] = relationship("Upload", back_populates="meta_spoorkabels")
    spoorkabel: Mapped[list["Spoorkabel"]] = relationship(
        "Spoorkabel", back_populates="meta_spoorkabel"
    )