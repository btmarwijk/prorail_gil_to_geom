from __future__ import annotations

from datetime import datetime, timedelta, timezone

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    field_serializer,
    field_validator,
)
from schemas.mappings import GROEP_MAPPING, SUBGROEP_MAPPING


class SpoorkabelBase(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    oud_nieuw: str | None = Field(
        default="OUD", alias="OUD/NIEUW", serialization_alias="oud_nieuw"
    )
    kabelnummer: int | None = Field(
        default=None, alias="KABELNUMMER", serialization_alias="kabelnummer"
    )
    kabel_geboren: datetime | str | int | None = Field(
        ..., alias="KABEL_GEBOREN", serialization_alias="kabel_geboren"
    )
    kabelnaam: str | None = Field(
        default=None, alias="KABELNAAM", serialization_alias="kabelnaam"
    )
    kabelnaam_oud: str | None = Field(
        default=None, alias="KABELNAAM_OUD", serialization_alias="kabelnaam_oud"
    )
    van: str | None = Field(default=None, alias="VAN", serialization_alias="van")
    naar: str | None = Field(default=None, alias="NAAR", serialization_alias="naar")
    kabeltype: str | None = Field(
        default=None, alias="KABELTYPE", serialization_alias="kabeltype"
    )

    groep: str | None = Field(default=None, alias="GROEP", serialization_alias="groep")
    sub_groep: str | None = Field(
        default=None, alias="SUB_GROEP", serialization_alias="sub_groep"
    )

    van_gil: str | None = Field(
        default=None, alias="VAN_GIL", serialization_alias="van_gil"
    )
    naar_gil: str | None = Field(
        default=None, alias="NAAR_GIL", serialization_alias="naar_gil"
    )

    geulen: str | None = Field(..., alias="GEULEN", serialization_alias="geulen")

    max_lengte: float | None = Field(
        default=None, alias="MAX_LENGTE", serialization_alias="max_lengte"
    )
    tb_lengte: float | None = Field(
        default=None, alias="TB_LENGTE", serialization_alias="tb_lengte"
    )
    ab_lengte: float | None = Field(
        default=None, alias="AB_LENGTE", serialization_alias="ab_lengte"
    )

    regelnummer: str | int | None = Field(
        default=None, alias="REGELNUMMER", serialization_alias="regelnummer"
    )

    @field_validator("kabel_geboren", mode="before")
    @classmethod
    def parse_date(cls, v):
        if isinstance(v, int):
            epoch = datetime(1970, 1, 1)
            return epoch + timedelta(seconds=v / 1000)
        if isinstance(v, str):
            try:
                dt = datetime.strptime(v, "%d-%m-%Y")
                return dt
            except ValueError:
                raise ValueError("Datum moet in dd-mm-yyyy formaat zijn")

    @field_serializer("kabel_geboren")
    def serialize_dt(self, dt: datetime | None):
        if dt is None:
            return None
        return int(dt.replace(tzinfo=timezone.utc).timestamp() * 1000)

    @field_validator("groep", mode="before")
    @classmethod
    def parse_groep(cls, v):
        if cls.__name__ != "SpoorkabelCreate":
            return v
        if isinstance(v, str):
            return GROEP_MAPPING.get(v, v)

    @field_validator("sub_groep", mode="before")
    def parse_subgroep(cls, v):
        if cls.__name__ != "SpoorkabelCreate":
            return v
        if isinstance(v, str):
            return SUBGROEP_MAPPING.get(v, v)


class SpoorkabelCreate(SpoorkabelBase):
    pass


class SpoorkabelRead(SpoorkabelBase):
    id: int
