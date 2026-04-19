from __future__ import annotations

from pydantic import BaseModel, ConfigDict

from .group_schemas import GroupRead
from .project_schemas import ProjectRead


class GroupProjectBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    group_id: int
    project_id: int


class GroupProjectCreate(GroupProjectBase):
    pass


class GroupProjectRead(GroupProjectBase):
    project: ProjectRead
    group: GroupRead
