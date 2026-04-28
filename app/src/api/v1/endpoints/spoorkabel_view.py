from core.database import get_db
from fastapi import APIRouter, Depends, HTTPException, Query
from geoalchemy2.shape import to_shape
from models import Spoorkabel
from schemas.spoorkabel_schema import SpoorkabelFeature
from sqlalchemy import func
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
