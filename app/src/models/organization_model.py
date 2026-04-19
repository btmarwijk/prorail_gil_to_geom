from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .group_model import Group
    from .organization_member_model import OrganizationMember
    from .project_model import Project


class Organization(Base):
    __tablename__ = "organization"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    slug: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    is_activate: Mapped[bool] = mapped_column(default=True)

    memberships: Mapped[list["OrganizationMember"]] = relationship(
        "OrganizationMember", back_populates="organization"
    )
    groups: Mapped[list["Group"]] = relationship("Group", back_populates="organization")
    projects: Mapped[list["Project"]] = relationship(
        "Project", back_populates="organization"
    )

    # TODO: Add AuditLogs, License, Quota and Invitaion
