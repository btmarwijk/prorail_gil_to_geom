from enums.organization_enums import EmailStatus
from models.base import Base
from models.mixins import TimestampMixin, UserOwnedMixin
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column


class EmailLog(TimestampMixin, UserOwnedMixin, Base):
    """A record of every email attempted by the system."""

    __tablename__ = "email_logs"

    id: Mapped[int] = mapped_column(primary_key=True)

    recipient_email: Mapped[str] = mapped_column(String(255), index=True)
    subject: Mapped[str] = mapped_column(String(255))
    template_name: Mapped[str] = mapped_column(String(100))  # e.g., "org_invitation"

    status: Mapped[EmailStatus] = mapped_column(String(20), default=EmailStatus.QUEUED)

    # External ID from providers like SendGrid, Mailgun, or AWS SES
    provider_id: Mapped[str | None] = mapped_column(String(255), index=True)
    error_details: Mapped[str | None] = mapped_column(String(1000))
