from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, Enum, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .enums import UserRole

if TYPE_CHECKING:
    from .group_membership_relation import GroupMembershipRelation
    from .group_model import Group
    from .upload_model import Upload
    from .user_login_model import UserLogin
    from .user_settings_model import UserSettings


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    role: Mapped[UserRole] = mapped_column(Enum(UserRole), default=UserRole.USER)

    email: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    first_name: Mapped[str | None] = mapped_column(String)
    last_name: Mapped[str | None] = mapped_column(String)
    validation_code: Mapped[str] = mapped_column(String(32), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    edited_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)

    uploads: Mapped[list["Upload"]] = relationship("Upload", back_populates="user")

    owned_groups: Mapped[list["Group"]] = relationship(
        "Group", back_populates="creator"
    )
    memberships: Mapped[list["GroupMembershipRelation"]] = relationship(
        "GroupMembershipRelation", back_populates="user"
    )

    user_settings: Mapped[UserSettings] = relationship(
        "UserSettings", back_populates="user"
    )
    user_logins: Mapped[UserLogin] = relationship("UserLogin", back_populates="user")
