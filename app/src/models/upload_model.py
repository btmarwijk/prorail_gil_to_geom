from __future__ import annotations
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING
from .base import Base

if TYPE_CHECKING:
    from .user_model import User
    from .meta_spoorkabel_model import MetaSpoorkabel

class Upload(Base):
    __tablename__ = "upload"
 
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
 
    tekeningnaam: Mapped[str | None] = mapped_column(String)
    versie: Mapped[str | None] = mapped_column(String)
    discipline: Mapped[str | None] = mapped_column(String)
    aantal_kabels: Mapped[int | None] = mapped_column(Integer)
    aantal_valide_kabels: Mapped[int | None] = mapped_column(Integer)
    download: Mapped[datetime | None] = mapped_column(DateTime)
    username: Mapped[str] = mapped_column("user", String, nullable=False)  # plain username string
    projectnaam: Mapped[str | None] = mapped_column(String)
    bestandnaam: Mapped[str | None] = mapped_column(String)
    processing_time: Mapped[str | None] = mapped_column(String)
    success: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
 
    user: Mapped["User"] = relationship("User", back_populates="uploads")
    meta_spoorkabels: Mapped[list["MetaSpoorkabel"]] = relationship(
        "MetaSpoorkabel", back_populates="upload"
    )