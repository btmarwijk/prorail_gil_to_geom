from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .group_project_relation import GroupProjectRelation
    from .organization_model import Organization
    from .tekening_model import Tekening


class Project(Base):
    __tablename__ = "projecten"

    id: Mapped[int] = mapped_column(primary_key=True)
    organization_id: Mapped[int] = mapped_column(ForeignKey("organization.id"))
    project_naam: Mapped[str] = mapped_column(String)
    created_at: Mapped[datetime] = mapped_column(DateTime)

    organization: Mapped["Organization"] = relationship(
        "Organization", back_populates="projects"
    )

    tekeningen: Mapped[list["Tekening"]] = relationship(
        "Tekening", back_populates="project"
    )

    groups: Mapped[list["GroupProjectRelation"]] = relationship(
        "GroupProjectRelation", back_populates="project"
    )
