from models.base import Base
from models.enums.organization_enums import JobState
from models.mixins import OrganizationOwnedMixin, TimestampMixin, UserOwnedMixin
from sqlalchemy import JSON, Float, String
from sqlalchemy.orm import Mapped, mapped_column


class JobStatus(TimestampMixin, UserOwnedMixin, OrganizationOwnedMixin, Base):
    """Tracks asynchronous background tasks (e.g., Geoprocessing)."""

    __tablename__ = "job_statuses"

    id: Mapped[int] = mapped_column(primary_key=True)

    job_type: Mapped[str] = mapped_column(
        String(50)
    )  # e.g., "geo_import", "report_generation"
    status: Mapped[JobState] = mapped_column(String(20), default=JobState.PENDING)

    # Progress tracking (0.0 to 100.0)
    progress: Mapped[float] = mapped_column(Float, default=0.0)

    # Store the result or error message here
    result: Mapped[dict | None] = mapped_column(JSON)
    error_message: Mapped[str | None] = mapped_column(String(1000))
