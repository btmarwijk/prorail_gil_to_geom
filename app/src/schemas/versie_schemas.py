from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel

from .tekening_schemas import TekeningRead


class VersieBase(BaseModel):
    tekening_id: int
    versie_nummer: str
    download_date: datetime
    geocodenaam: str
    regio: str | None = None


class VersieCreate(VersieBase):
    pass


class VersieRead(VersieBase):
    id: int
    tekening: TekeningRead | None = None
