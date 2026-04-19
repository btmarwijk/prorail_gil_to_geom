from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .mixins import TimestampMixin

if TYPE_CHECKING:
    from .tekening_model import Tekening
    from .user_model import User


class Upload(TimestampMixin, Base):
    __tablename__ = "upload"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)

    user: Mapped["User"] = relationship("User", back_populates="uploads")
    tekeningen: Mapped[list["Tekening"]] = relationship(
        "Tekening", back_populates="upload"
    )
