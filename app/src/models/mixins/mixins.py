from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, declared_attr, mapped_column, relationship

if TYPE_CHECKING:
    from models.organization_model import Organization
    from models.user_model import User


class TimestampMixin:
    """Provides created_at and edited_at columns automatically."""

    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    edited_at: Mapped[datetime] = mapped_column(
        DateTime, default=func.now(), onupdate=func.now()
    )


class UserOwnedMixin:
    @declared_attr
    def user_id(cls) -> Mapped[int]:
        return mapped_column(ForeignKey("user.id"), nullable=False)

    @declared_attr
    def owner(cls) -> Mapped["User"]:
        return relationship("User")


class OrganizationOwnedMixin:
    """
    Mixin to ensure a model belongs to an Organization.
    Enforces data isolation (Multi-tenancy).
    """

    # 1. The Foreign Key
    # nullable=False ensures every record MUST belong to an Org.
    # index=True is CRITICAL for performance when filtering by Org.
    @declared_attr
    def organization_id(cls) -> Mapped[int]:
        return mapped_column(
            ForeignKey("organization.id", ondelete="CASCADE"),
            nullable=False,
            index=True,
        )

    # 2. The Relationship
    # We use @declared_attr so each inheriting class gets its own relationship
    @declared_attr
    def organization(cls) -> Mapped["Organization"]:
        return relationship("Organization")
