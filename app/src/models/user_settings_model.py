from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import JSON, Boolean, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .user_model import User


class UserSettings(Base):
    __tablename__ = "user_settings"

    # One-to-One: The primary key is the user_id itself
    user_id: Mapped[int] = mapped_column(
        ForeignKey("user.id", ondelete="CASCADE"), primary_key=True
    )

    # --- UI & Experience ---
    dark_mode: Mapped[bool] = mapped_column(Boolean, default=False)
    language: Mapped[str] = mapped_column(String(10), default="nl")  # ISO 639-1 codes
    timezone: Mapped[str] = mapped_column(String(50), default="CET")
    compact_view: Mapped[bool] = mapped_column(Boolean, default=False)

    # --- Notification Toggles ---
    email_notifications: Mapped[bool] = mapped_column(Boolean, default=True)
    push_notifications: Mapped[bool] = mapped_column(Boolean, default=True)
    marketing_emails: Mapped[bool] = mapped_column(Boolean, default=False)

    # --- Privacy & Security ---
    profile_visible: Mapped[bool] = mapped_column(Boolean, default=True)
    show_online_status: Mapped[bool] = mapped_column(Boolean, default=True)

    # --- The "Catch-all" for future/custom settings ---
    # Using JSONB (Postgres) or JSON allows for schema-less settings
    # like specific dashboard layouts or widget positions.
    extra_config: Mapped[dict | None] = mapped_column(JSON, nullable=True)

    # Relationship back to User
    user: Mapped["User"] = relationship("User", back_populates="user_settings")
