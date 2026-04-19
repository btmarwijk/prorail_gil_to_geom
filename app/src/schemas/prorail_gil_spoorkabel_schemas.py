from __future__ import annotations

from pydantic import BaseModel, ConfigDict

from .prorail_gil_schema import ProrailGilRead
from .spoorkabel_versie_schema import SpoorkabelVersieRead


class SpoorkabelVersieProrailBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    spoorkabel_id: int
    prorail_feature_id: int


class SpoorkabelVersieProrailCreate(SpoorkabelVersieProrailBase):
    pass


class SpoorkabelVersieProrailRead(SpoorkabelVersieProrailBase):
    spoorkabel: SpoorkabelVersieRead
    prorail: ProrailGilRead
