from core import logger
from models.prorail_gil_model import ProrailGil
from models.spoorkabel_model import Spoorkabel
from models.spoorkabel_prorail_relation import SpoorkabelProrailRelation
from models.spoorkabel_versie_relation import SpoorkabelVersieDetail
from models.versie_model import Versie
from schemas.spoorkabel_schema import SpoorkabelCreate
from services.prorail_spoorkabel_service import ProrailSpoorkabelService
from sqlalchemy import func, select, update
from sqlalchemy.orm import Session, defer


class SpoorkabelService:
    def __init__(
        self, db: Session, spoorkabel_schemas: list[SpoorkabelCreate], versie: Versie
    ):
        self.db = db
        self.versie = versie
        self.spoorkabel_schemas = spoorkabel_schemas

    def insert_spoorkabel(self):
        logger.info("Inserting Spoorkabels")
        # 1. Extract all identifiers to fetch in one go
        kabelnummers = [s.kabelnummer for s in self.spoorkabel_schemas if s.kabelnummer]

        # 2. Bulk lookup existing VersieDetails
        existing_details_stmt = select(SpoorkabelVersieDetail).where(
            SpoorkabelVersieDetail.versie_id == self.versie.id,
            SpoorkabelVersieDetail.kabelnummer.in_(kabelnummers),
        )
        details_map = {
            d.kabelnummer: d for d in self.db.scalars(existing_details_stmt).all()
        }

        # 3. Fixed Statement
        existing_kabels_stmt = (
            select(Spoorkabel.kabelnummer)
            .join(Spoorkabel.versie_details)  # Join the relationship
            .where(SpoorkabelVersieDetail.id.in_([d.id for d in details_map.values()]))
        )
        existing_kabel_nums = set(self.db.scalars(existing_kabels_stmt).all())

        db_spoorkabels = []

        for schema in self.spoorkabel_schemas:
            if schema.kabelnummer in existing_kabel_nums:
                continue

            # Get or create detail from our local map instead of DB
            sv_detail = details_map.get(schema.kabelnummer)
            if not sv_detail:
                sv_detail = SpoorkabelVersieDetail(
                    versie_id=self.versie.id, kabelnummer=schema.kabelnummer
                )
                # No need to session.add(sv_detail) individually here,
                # SQLAlchemy handles it when you append it to the parent below.
                details_map[schema.kabelnummer] = sv_detail

            # Create the object WITHOUT 'versie_detail_id'
            new_kabel = Spoorkabel(
                **schema.model_dump(exclude_none=True),
            )

            # Use the SQLAlchemy relationship to link them
            new_kabel.versie_details.append(sv_detail)

            db_spoorkabels.append(new_kabel)

        # 4. Single transaction for everything
        self.db.add_all(db_spoorkabels)
        self.db.flush()

        self.spoorkabels = db_spoorkabels

    def insert_relates(self):
        service = ProrailSpoorkabelService(db=self.db, tekening=self.versie.tekening)
        stmt = (
            select(Spoorkabel)
            .join(Spoorkabel.versie_details)
            .where(SpoorkabelVersieDetail.versie_id == self.versie.id)
            .options(
                defer(Spoorkabel.geom)
            )  # <--- Prevents DB from sending heavy geometries
            .distinct()
        )
        _spoorkabels = self.db.scalars(stmt).all()
        logger.info("Starting processing relates: ")
        spoorkabels = service.process_all_kabels(_spoorkabels)
        logger.info("Starting Dissolve: ")
        self.dissolve_geometries_for_kabels(spoorkabels)

    def dissolve_geometries_for_kabels(self, kabels: list[Spoorkabel]):
        # 1. Extract IDs safely
        kabel_ids = [k.id for k in kabels if k.id is not None]

        if not kabel_ids:
            return  # Nothing to do if the list is empty or uncommitted

        # 2. Build the aggregate subquery
        # Equivalent to: SELECT spoorkabel_id, ST_Multi(ST_Union(geom)) AS dissolved_geom ...
        subq = (
            select(
                SpoorkabelProrailRelation.spoorkabel_id,
                func.ST_Multi(func.ST_Union(ProrailGil.geom)).label("dissolved_geom"),
            )
            .join(
                ProrailGil,
                SpoorkabelProrailRelation.prorail_feature_id == ProrailGil.id,
            )
            .where(
                ProrailGil.geom.is_not(None),
                SpoorkabelProrailRelation.spoorkabel_id.in_(
                    kabel_ids
                ),  # Filter by our specific list
            )
            .group_by(SpoorkabelProrailRelation.spoorkabel_id)
            .subquery()
        )

        # 3. Build the UPDATE statement
        # Equivalent to: UPDATE spoorkabel SET geom = subquery.dissolved_geom FROM subquery ...
        stmt = (
            update(Spoorkabel)
            .where(
                Spoorkabel.id == subq.c.spoorkabel_id
            )  # Join condition to the subquery
            .where(Spoorkabel.id.in_(kabel_ids))  # Belt-and-suspenders limit
            .values(geom=subq.c.dissolved_geom)
        )

        # 4. Execute and apply
        self.db.execute(stmt)

    def edit_spoorkabel(self):
        pass

    def remove_spoorkabel(self):
        pass
