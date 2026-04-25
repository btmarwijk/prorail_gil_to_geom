from __future__ import annotations

import re
import uuid
from datetime import date, datetime, timezone
from typing import Any, Literal

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    computed_field,
    field_serializer,
    field_validator,
)
from shapely.geometry import LineString, MultiLineString, shape


class SpatialReference(BaseModel):
    wkid: int
    latestWkid: int


class ArcGISPolyline(BaseModel):
    paths: list[list[list[float]]]
    spatialReference: SpatialReference | None = None

    @computed_field
    def wkt(self) -> str:
        """Converts ArcGIS paths to a PostGIS-ready MULTILINESTRING WKT."""
        if not self.paths:
            return "MULTILINESTRING EMPTY"

        # Convert to shapely via the __geo_interface__ style dict
        # ArcGIS 'paths' translates to MultiLineString in geo_interface
        shapely_geom = shape({"type": "MultiLineString", "coordinates": self.paths})

        # Ensure it is a MultiLineString for database consistency
        if isinstance(shapely_geom, LineString):
            shapely_geom = MultiLineString([shapely_geom])

        return shapely_geom.wkt


class ProrailAttributesCreate(BaseModel):
    """Alle Features/Objecten van de Prorail FeatureServer delen deze attributen"""

    model_config = ConfigDict(populate_by_name=True)

    tekeningnaam: str = Field(
        ..., alias="TEKENINGNAAM", serialization_alias="tekeningnaam"
    )
    tekeningversie: str = Field(
        ..., alias="TEKENINGVERSIE", serialization_alias="tekeningversie"
    )
    gil_nummer: int = Field(..., alias="GILNUMMER", serialization_alias="gil_nummer")
    opmerking: str | None = Field(
        ..., alias="OPMERKING", serialization_alias="opmerking"
    )
    plaatsingsdatum: datetime | str | None = Field(
        ..., alias="PLAATSINGSDATUM", serialization_alias="plaatsingsdatum"
    )
    feature_type: str | None = Field(default=None)
    spoorkabel_guid: str | None = Field(default=None)
    shape_length: float | None = Field(
        default=None, alias="Shape__Length", exclude=True
    )

    @field_validator("plaatsingsdatum", mode="before")
    @classmethod
    def parse_timestamp(cls, v):
        if isinstance(v, (int, float)):
            if v <= 0:
                return None
            try:
                return datetime.fromtimestamp(v / 1000, tz=timezone.utc)
            except (OSError, OverflowError, ValueError):
                return None
        if isinstance(v, str) and v == "":
            return None

    @field_serializer("plaatsingsdatum")
    def to_timestamp(self, v: Any):
        if isinstance(v, int):
            return v

        if isinstance(v, (datetime, date)):
            dt = (
                v
                if isinstance(v, datetime)
                else datetime.combine(v, datetime.min.time())
            )
            return int(dt.replace(tzinfo=timezone.utc).timestamp() * 1000)

        if isinstance(v, str):
            try:
                dt = datetime.strptime(v, "%d-%m-%Y")
                return int(dt.replace(tzinfo=timezone.utc).timestamp() * 1000)
            except ValueError:
                return None

        return None

    @computed_field
    @property
    def discipline(self) -> Literal["KS", "WB", "WV", "RD"]:
        if not self.tekeningnaam:
            return None

        match = re.search(r"\b(KS|WB|WV|RD)\b", self.tekeningnaam)

        if match:
            return match.group(0)

        return None


class ProrailAttributesRead(ProrailAttributesCreate):
    object_id: int = Field(..., alias="OBJECTID")
    global_id: uuid.UUID = Field(..., alias="GlobalID")

    @field_validator("global_id", mode="before")
    @classmethod
    def str_to_uuid(cls, v: any) -> uuid.UUID:
        if isinstance(v, str):
            clean_uuid = v.strip().strip("{}")
            return uuid.UUID(clean_uuid)
        return v

    @field_serializer("global_id")
    def uuid_to_string(self, global_id) -> str:
        return str(global_id)


class FeatureCreate(BaseModel):
    attributes: ProrailAttributesCreate
    geometry: ArcGISPolyline

    @field_serializer("geometry")
    def serialize_geom_to_wkt(self, geom: ArcGISPolyline) -> str:
        # Zero-dependency version (no shapely required)
        formatted_paths = []
        for path in geom.paths:
            # Join points with space, then join coordinates with comma
            points = ", ".join([f"{p[0]} {p[1]}" for p in path])
            formatted_paths.append(f"({points})")

        inner_wkt = ", ".join(formatted_paths)
        return f"MULTILINESTRING ({inner_wkt})"


class FeatureRead(BaseModel):
    attributes: ProrailAttributesRead
    geometry: ArcGISPolyline
