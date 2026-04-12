from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .group_membership_relation import GroupMembershipRelation
    from .group_project_relation import GroupProjectRelation
    from .user_model import User


class Group(Base):
    __tablename__ = "groups"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    creator_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    creator: Mapped["User"] = relationship("User", back_populates="owned_groups")

    members: Mapped[list["GroupMembershipRelation"]] = relationship(
        "GroupMembershipRelation", back_populates="group"
    )

    projects: Mapped[list["GroupProjectRelation"]] = relationship(
        "GroupProjectRelation", back_populates="user"
    )
