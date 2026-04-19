from __future__ import annotations

from datetime import datetime

from models.enums import UserRole
from pydantic import BaseModel, EmailStr

from .group_membership_schemas import GroupMembershipRead
from .group_schemas import GroupRead
from .upload_schemas import UploadRead


class UserBase(BaseModel):
    id: int
    email: EmailStr
    role: UserRole


class UserCreate(UserBase):
    pass


class UserRead(BaseModel):
    created_at: datetime

    uploads: list["UploadRead"] = []
    owned_groups: list["GroupRead"] = []
    memberships: list["GroupMembershipRead"] = []
