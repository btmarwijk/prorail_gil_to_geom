from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from .prorail_gil_spoorkabel_schemas import SpoorkabelVersieProrailRead
from .tekening_schemas import TekeningRead


class ProrailGilBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    tekeningnaam: str = Field(..., max_length=16)
    tekeningversie: str = Field(..., max_length=8)
    gil_nummer: int
    opmerking: str | None = Field(default=None, max_length=1000)
    plaatsingsdatum: datetime | None = None
    feature_type: str | None = Field(default=None, max_length=32)
    discipline: str | None = None

    geom: Any | None = None


class ProrailGilCreate(ProrailGilBase):
    pass


class ProrailGilRead(ProrailGilBase):
    id: int
    tekening: TekeningRead | None = None
    spoorkabel_versies: list[SpoorkabelVersieProrailRead]
