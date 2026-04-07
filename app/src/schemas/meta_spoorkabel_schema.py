import re
from datetime import datetime, timedelta, timezone

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    computed_field,
    field_serializer,
    field_validator,
)
from schemas.mappings import GROEP_MAPPING, SUBGROEP_MAPPING
from utils.default_factory_functions import utc_now_ms


class MetaSpoorkabelCreate(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    tekeningnaam: str
    versie: str
    geocodenaam: str
    gedownload: datetime | str | int | None = None
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

    created_at: datetime | int = Field(..., default_factory=utc_now_ms)

    upload_guid: str | None

    @field_validator("kabel_geboren", "gedownload", mode="before")
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

    @field_serializer("kabel_geboren", "gedownload")
    def serialize_dt(self, dt: datetime | None):
        if dt is None:
            return None
        return int(dt.replace(tzinfo=timezone.utc).timestamp() * 1000)

    @field_validator("groep", mode="before")
    @classmethod
    def parse_groep(cls, v):
        if cls.__name__ != "MetaSpoorkabelCreate":
            return v

        if isinstance(v, str):
            return GROEP_MAPPING.get(v, v)

    @field_validator("sub_groep", mode="before")
    def parse_subgroep(cls, v):
        if cls.__name__ != "MetaSpoorkabelCreate":
            return v

        if isinstance(v, str):
            return SUBGROEP_MAPPING.get(v, v)

    @computed_field
    @property
    def unique_key(self) -> str:
        return f"{self.oud_nieuw}{self.tekeningnaam}{self.kabelnummer}"

    @computed_field
    @property
    def discipline(self) -> str:
        if not self.tekeningnaam:
            return None

        match = re.search(r"\b(KS|WB|WV|RD)\b", self.tekeningnaam)

        if match:
            return match.group(0)

        return None


class MetaSpoorkabelRead(MetaSpoorkabelCreate):
    # TODO: Change to object_id
    geulen: list[int] | None = Field(..., alias="geulen")

    @field_validator("geulen", mode="before")
    @classmethod
    def parse_geulen(cls, v):
        if isinstance(v, str):
            return [int(x) for x in v.split()]
        return v
