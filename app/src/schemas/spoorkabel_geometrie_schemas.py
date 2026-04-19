from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class SpoorkabelGeometrieBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    versie_details_id: int
    geom: Any
    geometry_hash: str = Field(..., max_length=64)


class SpoorkabelGeometrieCreate(SpoorkabelGeometrieBase):
    pass


class SpoorkabelGeometrieRead(SpoorkabelGeometrieBase):
    id: int
