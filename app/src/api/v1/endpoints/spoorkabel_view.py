from core.database import get_db
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import JSONResponse
from geoalchemy2.shape import to_shape
from models import Spoorkabel
from schemas.spoorkabel_schema import (
    SpoorkabelFeature,
)
from sqlalchemy import cast, func, literal_column
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Session

router = APIRouter()


@router.get("/spoorkabel/{spoorkabel_id}", response_model=SpoorkabelFeature)
def read_sporkabel(
    spoorkabel_id: int, epsg: int = Query(4326), db: Session = Depends(get_db)
):
    spoorkabel, transformed_geom = (
        db.query(Spoorkabel, func.ST_Transform(Spoorkabel.geom, epsg))
        .filter(Spoorkabel.id == spoorkabel_id)
        .first()
    )

    if spoorkabel is None:
        raise HTTPException(status_code=404, detail="Spoorkabel niet gevonden")

    return SpoorkabelFeature(
        type="Feature", geometry=to_shape(transformed_geom), properties=spoorkabel
    )


@router.get("/spoorkabels/all")
def read_all_spoorkabels(
    epsg: int = Query(4326),
    db: Session = Depends(get_db),
    limit: int = 100,
    offset: int = 0,
):
    tolerance = 1 if epsg != 4326 else 0.000010

    # 1. Transform and Simplify Geometry
    geom_expr = func.ST_SimplifyPreserveTopology(
        func.ST_Transform(Spoorkabel.geom, epsg), tolerance
    )

    # 2. Let PostGIS build the entire GeoJSON Feature object.
    # `to_jsonb(Spoorkabel) - 'geom'` converts the row to a JSON object
    # and safely strips out the heavy geometry column from the properties.
    feature_expr = func.jsonb_build_object(
        "type",
        "Feature",
        "geometry",
        cast(func.ST_AsGeoJSON(geom_expr), JSONB),
        # Use the table object and cast it to jsonb
        "properties",
        func.to_jsonb(literal_column(Spoorkabel.__tablename__)) - "geom",
    )

    # 3. Query the pre-compiled JSON directly from the database
    results = (
        db.query(feature_expr)
        .filter(Spoorkabel.geom.isnot(None))
        .order_by(Spoorkabel.id)
        .offset(offset)
        .limit(limit)
        .all()
    )

    # 4. Construct the Parent FeatureCollection
    # 'results' is a list of tuples containing dictionaries: [({"type": "Feature", ...},), ...]
    feature_collection = {
        "type": "FeatureCollection",
        "features": [row[0] for row in results],
    }

    # 5. Return directly via JSONResponse (skipping Pydantic completely)
    return JSONResponse(content=feature_collection)


# @router.get("/spoorkabels/{tekeningnaam}", response_model=SpoorkabelFeature)
# def read_spoorkabels(
#     tekeningnaam: str, epsg: int = Query(4326), db: Session = Depends(get_db)
# ):
#     tekening = (
#         db.query(Tekening)
#         .options(joinedload(Tekening.versies))
#         .where(Tekening.naam == tekeningnaam)
#         .first()
#     )
#
#     pass
