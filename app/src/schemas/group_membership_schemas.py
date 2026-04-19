from __future__ import annotations

from pydantic import BaseModel, ConfigDict

from .group_schemas import GroupRead
from .user_schemas import UserRead


class GroupMembershipBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    user_id: int
    group_id: int


class GroupMembershipCreate(GroupMembershipBase):
    pass


class GroupMembershipRead(GroupMembershipBase):
    user: UserRead
    group: GroupRead
