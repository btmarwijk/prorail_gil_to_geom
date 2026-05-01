from models.prorail_gil_model import ProrailGil
from models.spoorkabel_model import Spoorkabel
from models.spoorkabel_prorail_relation import SpoorkabelProrailRelation
from models.tekening_model import Tekening
from sqlalchemy import select
from sqlalchemy.orm import Session


class ProrailSpoorkabelService:
    def __init__(self, db: Session, tekening: Tekening):
        self.db = db
        self.tekening_id = tekening.id
        self.tekeningnaam = tekening.naam

    def process_all_kabels(self, spoorkabels: list[Spoorkabel]) -> list[Spoorkabel]:
        """
        Processes a batch of kabels in bulk to establish Prorail relations.
        """
        # 1. Extract ALL unique geul IDs across ALL kabels in one go
        all_geul_ids = set()
        for kabel in spoorkabels:
            if kabel.geulen:
                all_geul_ids.update(kabel.geulen)

        if not all_geul_ids:
            return spoorkabels

        # 2. BULK FETCH existing ProrailGil features in a single query
        stmt = select(ProrailGil).where(
            ProrailGil.gil_nummer.in_(all_geul_ids),
            ProrailGil.tekening_id == self.tekening_id,
        )
        existing_gils = self.db.scalars(stmt).all()

        # Create a fast Python dictionary lookup: {gil_nummer: ProrailGil_object}
        gil_map = {gil.gil_nummer: gil for gil in existing_gils}

        # 3. BULK CREATE missing ProrailGil objects
        missing_ids = all_geul_ids - set(gil_map.keys())
        new_gils = []

        for missing_id in missing_ids:
            new_gils.append(
                ProrailGil(
                    gil_nummer=missing_id,
                    tekeningnaam=self.tekeningnaam,
                    tekening_id=self.tekening_id,
                    tekeningversie="N/A",
                    feature_type="Auto-generated",
                    is_existing=False,
                )
            )

        # Flush ONLY ONCE to generate IDs for the newly created features
        if new_gils:
            self.db.add_all(new_gils)
            self.db.flush()
            # Add the newly created ones to our lookup map
            for new_gil in new_gils:
                gil_map[new_gil.gil_nummer] = new_gil

        # 4. Link the relations in memory
        for kabel in spoorkabels:
            if not kabel.geulen:
                continue

            # Extract IDs of already linked gils to prevent lazy-loading lookups
            # Assumes kabel.prorail_gils is loaded (or safe to load once per kabel)
            existing_linked_ids = {rel.prorail_gil_id for rel in kabel.prorail_gils}

            for geul_id in set(kabel.geulen):
                prorail_feature = gil_map[geul_id]

                # Check against the pre-calculated set of IDs
                if prorail_feature.id not in existing_linked_ids:
                    new_relation = SpoorkabelProrailRelation(
                        spoorkabel=kabel, prorail_gil=prorail_feature
                    )
                    self.db.add(new_relation)
                    # Update local set in case of duplicates within the same process
                    existing_linked_ids.add(prorail_feature.id)

        # 5. Commit everything at once
        self.db.commit()

        # NOTE: I removed the loop with `self.db.refresh(kabel)`.
        # Refreshing in a loop causes an N+1 query issue. If you absolutely
        # need the refreshed objects, it's better to run a new `select().in_()`
        # query for them, or simply trust the ORM's in-memory state.

        return spoorkabels
