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

    def link_geulen_to_prorail(self, spoorkabel: Spoorkabel):
        """
        Processes the geulen list for a single Spoorkabel and establishes relations.
        """
        if not spoorkabel.geulen or len(spoorkabel.geulen) == 0:
            return

        unique_geulen = set(spoorkabel.geulen)

        for geul_id in unique_geulen:
            # 1. Attempt to find existing ProrailGil
            stmt = select(ProrailGil).where(
                ProrailGil.gil_nummer == geul_id,
                ProrailGil.tekening_id == self.tekening_id,
            )
            prorail_feature = self.db.scalars(stmt).first()

            # 2. If not found, create a new record
            if not prorail_feature:
                prorail_feature = ProrailGil(
                    gil_nummer=geul_id,
                    tekeningnaam=self.tekeningnaam,
                    tekening_id=self.tekening_id,
                    tekeningversie="N/A",  # Required by your model
                    feature_type="Auto-generated",
                    is_existing=False,  # Custom flag requested
                )
                self.db.add(prorail_feature)
                # Flush to get an ID for the relation table without committing yet
                self.db.flush()

            # 3. Check if the relation already exists to avoid duplicates
            relation_exists = any(
                rel.prorail_feature_id == prorail_feature.id
                for rel in spoorkabel.prorail_gils
            )

            if not relation_exists:
                new_relation = SpoorkabelProrailRelation(
                    spoorkabel=spoorkabel, prorail_gil=prorail_feature
                )
                self.db.add(new_relation)

    def process_all_kabels(self, spoorkabels: list[Spoorkabel]) -> list[Spoorkabel]:
        """
        Processes a batch of kabels and returns the updated list.
        """
        for kabel in spoorkabels:
            self.link_geulen_to_prorail(kabel)

        # 1. Commit all changes to the DB
        self.db.commit()

        # 2. Refresh the objects (Optional but recommended)
        # This ensures that if you access 'kabel.prorail_gils' later,
        # SQLAlchemy knows to fetch the newly created relations from the DB.
        for kabel in spoorkabels:
            self.db.refresh(kabel)

        return spoorkabels
