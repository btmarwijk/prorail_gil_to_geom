from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .mixins import TimestampMixin

if TYPE_CHECKING:
    from .organization_model import Organization
    from .user_model import User


class OrganizationMember(TimestampMixin, Base):
    __tablename__ = "organization_members"

    organization_id: Mapped[int] = mapped_column(
        ForeignKey("organization.id", ondelete="CASCADE"), primary_key=True
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("user.id", ondelete="CASCADE"), primary_key=True
    )

    # Organization-specific role (e.g., "owner", "admin", "member")
    org_role: Mapped[str] = mapped_column(String(20), default="member")

    organization: Mapped["Organization"] = relationship(
        "Organization", back_populates="memberships"
    )
    user: Mapped["User"] = relationship(
        "User", back_populates="organization_memberships"
    )
