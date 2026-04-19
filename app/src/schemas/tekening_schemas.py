from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict

from .versie_schemas import VersieRead


class TekeningBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    upload_id: int
    project_id: int
    naam: str
    bestandnaam: Optional[str] = None
    processing_time: Optional[str] = None
    success: str


class TekeningCreate(TekeningBase):
    pass


class TekeningRead(TekeningBase):
    id: int
    created_at: datetime
    versies: List[VersieRead] = []
