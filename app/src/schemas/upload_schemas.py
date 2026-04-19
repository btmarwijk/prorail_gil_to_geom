from __future__ import annotations

from pydantic import BaseModel, ConfigDict

from .tekening_schemas import TekeningRead


class UploadBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    user_id: int


class UploadCreate(UploadBase):
    pass


class UploadRead(UploadBase):
    id: int
    tekeningen: list[TekeningRead] = []
