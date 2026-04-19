from datetime import datetime
from typing import TYPE_CHECKING

from models.base import Base
from models.mixins import OrganizationOwnedMixin, TimestampMixin, UserOwnedMixin
from sqlalchemy import JSON, DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

if TYPE_CHECKING:
    pass


class AuditLog(TimestampMixin, UserOwnedMixin, OrganizationOwnedMixin, Base):
    """A read-only record of all significant actions in the system."""

    __tablename__ = "audit_logs"

    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    action: Mapped[str] = mapped_column(String(100))  # "project.deleted"
    target_type: Mapped[str] = mapped_column(String(50))  # e.g., "Project", "Group"
    target_id: Mapped[int | None] = mapped_column(Integer)

    # Stores the before/after state or extra context
    payload: Mapped[dict | None] = mapped_column(JSON)
    ip_address: Mapped[str | None] = mapped_column(String(45))
