from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, DateTime, ForeignKey, Index, String, Text
from sqlalchemy.dialects.postgresql import INET
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .user_model import User


class UserLogin(Base):
    __tablename__ = "user_logins"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("user.id", ondelete="CASCADE"), nullable=False, index=True
    )

    # Authentication details
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    is_success: Mapped[bool] = mapped_column(Boolean, default=True)

    # Contextual data (Where and How)
    # Using INET for Postgres allows for built-in subnet searching
    ip_address: Mapped[str] = mapped_column(INET, nullable=True)
    user_agent: Mapped[str | None] = mapped_column(Text)  # Browser/Device info

    # Geolocation (Populated via background task from IP)
    location_city: Mapped[str | None] = mapped_column(String(100))
    location_country: Mapped[str | None] = mapped_column(String(100))

    # Session tracking
    auth_method: Mapped[str] = mapped_column(
        String(50)
    )  # 'password', 'google_oauth', 'magic_link'

    # Relationship back to User
    user: Mapped["User"] = relationship("User", back_populates="login_history")

    # Add an index on (user_id, timestamp) for fast history lookups
    __table_args__ = (Index("ix_user_login_user_time", "user_id", "timestamp"),)
