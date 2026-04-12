from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .group_model import Group
    from .user_model import User


class GroupMembershipRelation(Base):
    __tablename__ = "group_members"

    user_id: Mapped[int] = mapped_column(
        ForeignKey("user.id", ondelete="CASCADE"), primary_key=True
    )

    group_id: Mapped[int] = mapped_column(
        ForeignKey("groups.id", ondelete="CASCADE"), primary_key=True
    )

    user: Mapped["User"] = relationship("User", back_populates="memberships")

    group: Mapped["Group"] = relationship("Group", back_populates="members")
