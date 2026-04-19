from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict

from .group_projects_schemas import GroupProjectRead
from .tekening_schemas import TekeningRead


class ProjectBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    project_naam: str


class ProjectCreate(ProjectBase):
    pass


class ProjectRead(ProjectBase):
    id: int
    created_at: datetime
    tekeningen: list[TekeningRead] = []
    groups: list[GroupProjectRead] = []
