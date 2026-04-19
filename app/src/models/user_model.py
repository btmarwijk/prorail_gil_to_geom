from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import Enum, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .enums import UserRole
from .mixins import TimestampMixin

if TYPE_CHECKING:
    from .group_membership_relation import GroupMembershipRelation
    from .group_model import Group
    from .organization_member_model import OrganizationMember
    from .upload_model import Upload
    from .user_login_model import UserLogin
    from .user_settings_model import UserSettings


class User(TimestampMixin, Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    role: Mapped[UserRole] = mapped_column(Enum(UserRole), default=UserRole.USER)

    email: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    first_name: Mapped[str | None] = mapped_column(String)
    last_name: Mapped[str | None] = mapped_column(String)

    uploads: Mapped[list["Upload"]] = relationship("Upload", back_populates="user")

    owned_groups: Mapped[list["Group"]] = relationship(
        "Group", back_populates="creator"
    )
    memberships: Mapped[list["GroupMembershipRelation"]] = relationship(
        "GroupMembershipRelation", back_populates="user"
    )

    organization_memberships: Mapped[list["OrganizationMember"]] = relationship(
        "OrganizationMember", back_populates="user"
    )

    user_settings: Mapped[UserSettings] = relationship(
        "UserSettings", back_populates="user"
    )
    user_logins: Mapped[list[UserLogin]] = relationship(
        "UserLogin", back_populates="user"
    )
