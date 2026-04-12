from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .group_model import Group
    from .project_model import Project


class GroupProjectRelation(Base):
    __tablename__ = "group_project_relations"

    group_id: Mapped[int] = mapped_column(
        ForeignKey("groups.id", ondelete="CASCADE"), primary_key=True
    )

    project_id: Mapped[int] = mapped_column(
        ForeignKey("projecten.id", ondelete="CASCADE"), primary_key=True
    )

    group: Mapped["Group"] = relationship("Group", back_populates="projects")

    project: Mapped["Project"] = relationship("Project", back_populates="groups")
