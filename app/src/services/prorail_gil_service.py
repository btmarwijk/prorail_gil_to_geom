import re
from types import MappingProxyType
from typing import Literal

from arcgis.features import FeatureLayer, FeatureSet
from core.config import settings
from models.prorail_gil_model import ProrailGil
from models.tekening_model import Tekening
from schemas.prorail_gil_schema import FeatureCreate
from sqlalchemy import delete, select
from sqlalchemy.orm import Session


class ProrailPublicFeatureLayer:
    _registry: dict[str, type["ProrailPublicFeatureLayer"]] = {}

    base_url: str = ""
    prorail_feature_layers: dict[str, str] = {}

    def __init_subclass__(cls, discipline: str, **kwargs):
        super().__init_subclass__(**kwargs)
        cls._registry[discipline] = cls

    @classmethod
    def get_layer(
        cls, discipline: Literal["KS", "RD", "WV", "WB"]
    ) -> "ProrailPublicFeatureLayer":
        layer_class = cls._registry.get(discipline)
        if not layer_class:
            raise ValueError(f"Onbekende discipline: {discipline}")
        return layer_class()

    def get_by_tekeningnaam(self, tekeningnaam: str) -> list[FeatureCreate]:
        where = f"TEKENINGNAAM = '{tekeningnaam}'"
        all_results: list[FeatureCreate] = []

        for layer_nr, feature_type in self.prorail_feature_layers.items():
            layer = FeatureLayer(f"{self.base_url}/{layer_nr}")
            feature_set: FeatureSet = layer.query(
                where=where, out_fields="*", return_geometry=True
            )

            for f in feature_set.features:
                f.attributes["feature_type"] = feature_type
                all_results.append(FeatureCreate(**f.as_dict))

        return all_results


class KabelSituatieLayer(ProrailPublicFeatureLayer, discipline="KS"):
    base_url: str = settings.PRORAIL_FEATURE_SERVER_KS

    prorail_feature_layers = MappingProxyType(
        {
            "14": "Kokertracé",
            "15": "Tijdelijke buis",
            "16": "Geul",
            "17": "Spoorkruising",
            "18": "Waterkruising",
            "19": "Wegkruising",
        }
    )


class RioolDrainageLayer(ProrailPublicFeatureLayer, discipline="RD"):
    base_url: str = settings.PRORAIL_FEATURE_SERVER_RD

    prorail_feature_layers = MappingProxyType(
        {
            "5": "Kokertracé",
            "6": "Tijdelijke buis",
            "7": "Geul",
            "8": "Spoorkruising",
            "9": "Waterkruising",
            "10": "Wegkruising",
        }
    )


class WaterBrandleidingLayer(ProrailPublicFeatureLayer, discipline="WB"):
    base_url = settings.PRORAIL_FEATURE_SERVER_WB

    prorail_feature_layers = MappingProxyType(
        {
            "5": "Kokertracé",
            "6": "Tijdelijke buis",
            "7": "Geul",
            "8": "Spoorkruising",
            "9": "Waterkruising",
            "10": "Wegkruising",
        }
    )


class WisselverwarmingLayer(ProrailPublicFeatureLayer, discipline="WV"):
    base_url = settings.PRORAIL_FEATURE_SERVER_WV

    prorail_feature_layers = MappingProxyType(
        {
            "6": "Kokertracé",
            "7": "Tijdelijke buis",
            "8": "Geul",
            "9": "Spoorkruising",
            "10": "Waterkruising",
            "11": "Wegkruising",
        }
    )


class ProrailFeatureService:
    def __init__(self, db: Session):
        self.db = db

    def _extract_discipline(self, tekeningnaam: str) -> str:
        match = re.search(r"(KS|WB|WV|RD)", tekeningnaam.upper())
        if not match:
            raise ValueError(f"No valid discipline found in: {tekeningnaam}")
        return match.group(0)

    def sync_features_by_tekening(self, tekening: Tekening):
        # 1. Identify Discipline
        discipline = self._extract_discipline(tekening.naam)
        layer_provider = ProrailPublicFeatureLayer.get_layer(discipline)

        # 2. Fetch from ArcGIS
        features = layer_provider.get_by_tekeningnaam(tekening.naam)
        if not features:
            print(f"No features found for {tekening.naam}")
            return []

        # 3. Check Version (Compare first response feature with DB)
        new_version = features[0].attributes.tekeningversie

        # Query for the version of existing records in the DB
        existing_stmt = (
            select(ProrailGil.tekeningversie)
            .where(ProrailGil.tekening_id == tekening.id)
            .limit(1)
        )
        current_db_version = self.db.execute(existing_stmt).scalar_one_or_none()

        # 4. Version Logic
        if current_db_version:
            if new_version == current_db_version:
                print(f"Version {new_version} already exists in DB. Skipping sync.")
                return []

            # Python string comparison works for versions like 'A' < 'B' or '1' < '2'
            if new_version > current_db_version:
                print(
                    f"New version found ({new_version} > {current_db_version}). Updating records..."
                )
                # Delete old records to make room for new ones
                self.db.execute(
                    delete(ProrailGil).where(ProrailGil.tekening_id == tekening.id)
                )
            else:
                print(
                    f"DB version ({current_db_version}) is newer than API version ({new_version}). Skipping."
                )
                return []

        # 5. Process and Insert
        db_objects = []
        for feat in features:
            attrs = feat.attributes
            new_record = ProrailGil(
                tekening_id=tekening.id,
                geom=f"SRID=28992;{feat.geometry.wkt}",
                tekeningnaam=attrs.tekeningnaam,
                tekeningversie=attrs.tekeningversie,
                gil_nummer=attrs.gil_nummer,
                opmerking=attrs.opmerking,
                plaatsingsdatum=attrs.plaatsingsdatum,
                feature_type=attrs.feature_type,
            )
            db_objects.append(new_record)

        if db_objects:
            self.db.add_all(db_objects)
            self.db.flush()
            print(
                f"Successfully synced {len(db_objects)} features (Version: {new_version})"
            )

        return db_objects


if __name__ == "__main__":
    from core.database import SessionLocal

    # Setup database session
    db = SessionLocal()

    try:
        # Example: Suppose we just created drawing ID 1 for '560KS01'
        target_tekening_id = 1
        target_naam = "560KS01"

        # Initialize the service
        geo_service = ProrailFeatureService(db)

        # Fetch and Save
        results = geo_service.sync_features_by_tekening(
            tekening_id=target_tekening_id, tekeningnaam=target_naam
        )

        if results:
            print(f"First record ID: {results[0].id}")

    except Exception as e:
        db.rollback()
        print(f"Error during sync: {e}")
    finally:
        db.close()
