from datetime import datetime

from models.base import Base
from models.enums.organization_enums import LicenseStatus
from models.mixins import OrganizationOwnedMixin, TimestampMixin
from sqlalchemy import DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship


class License(TimestampMixin, OrganizationOwnedMixin, Base):
    __tablename__ = "licenses"

    id: Mapped[int] = mapped_column(primary_key=True)

    plan_name: Mapped[str] = mapped_column(String(50))  # e.g., "Enterprise", "Pro"
    status: Mapped[LicenseStatus] = mapped_column(
        String(20), default=LicenseStatus.TRIAL
    )

    starts_at: Mapped[datetime] = mapped_column(DateTime)
    expires_at: Mapped[datetime | None] = mapped_column(DateTime)

    quota: Mapped["Quota"] = relationship(
        "Quota", back_populates="license", uselist=False
    )


class Quota(TimestampMixin, Base):
    """Tracks the hard limits for an organization based on their license."""

    __tablename__ = "quotas"

    id: Mapped[int] = mapped_column(primary_key=True)
    license_id: Mapped[int] = mapped_column(ForeignKey("licenses.id"), unique=True)

    max_projects: Mapped[int] = mapped_column(Integer, default=5)
    max_users: Mapped[int] = mapped_column(Integer, default=10)
    storage_limit_gb: Mapped[int] = mapped_column(Integer, default=1)

    license: Mapped["License"] = relationship("License", back_populates="quota")
