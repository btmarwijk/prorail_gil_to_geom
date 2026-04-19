from __future__ import annotations

from pydantic import BaseModel

from .spoorkabel_geometrie_schemas import SpoorkabelGeometrieRead
from .spoorkabel_schema import SpoorkabelRead
from .versie_schemas import VersieRead


class SpoorkabelVersieBase(BaseModel):
    id: int
    kabel_id: int
    versie_id: int
    geometrie_id: int | None = None
    status: str
    lengte: float | None = None


class SpoorkabelVersieCreate(SpoorkabelVersieBase):
    pass


class SpoorkabelVersieRead(SpoorkabelVersieBase):
    spoorkabel: SpoorkabelRead
    versie: VersieRead
    geometrie: SpoorkabelGeometrieRead | None = None
