from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .tekening_model import Tekening
    from .user_model import User


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
    projectnaam: Mapped[str | None] = mapped_column(String)
    bestandnaam: Mapped[str | None] = mapped_column(String)
    processing_time: Mapped[str | None] = mapped_column(String)
    success: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    user: Mapped["User"] = relationship("User", back_populates="uploads")
    tekeningen: Mapped[list["Tekening"]] = relationship(
        "Tekening", back_populates="upload"
    )
