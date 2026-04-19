import uuid
from datetime import datetime

from models.base import Base
from models.enums.organization_enums import InvitationStatus
from models.mixins import OrganizationOwnedMixin, TimestampMixin, UserOwnedMixin
from sqlalchemy import DateTime, String
from sqlalchemy.orm import Mapped, mapped_column


class Invitation(TimestampMixin, UserOwnedMixin, OrganizationOwnedMixin, Base):
    __tablename__ = "invitations"

    id: Mapped[int] = mapped_column(primary_key=True)
    token: Mapped[str] = mapped_column(
        String(64), unique=True, default=lambda: str(uuid.uuid4())
    )

    email: Mapped[str] = mapped_column(String(255), index=True)
    role: Mapped[str] = mapped_column(String(20), default="member")
    status: Mapped[InvitationStatus] = mapped_column(
        String(20), default=InvitationStatus.PENDING
    )

    expires_at: Mapped[datetime] = mapped_column(DateTime)
