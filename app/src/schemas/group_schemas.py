from __future__ import annotations

from typing import List

from pydantic import BaseModel, ConfigDict

from .group_membership_schemas import GroupMembershipRead
from .group_projects_schemas import GroupProjectRead


class GroupBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    name: str
    creator_id: int


class GroupCreate(GroupBase):
    pass


class GroupRead(GroupBase):
    id: int
    members: List["GroupMembershipRead"] = []
    projects: List["GroupProjectRead"] = []
