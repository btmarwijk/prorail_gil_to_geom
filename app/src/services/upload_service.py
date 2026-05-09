from dataclasses import asdict

from core import logger
from models import (
    Tekening,
    Upload,
    User,
    Versie,
    VersieBestaand,
    VersieOntwerp,
    VersieOntwerpFase,
)
from schemas.spoorkabel_schema import SpoorkabelCreate
from services.prorail_gil_service import ProrailFeatureService
from services.spoorkabel_service import SpoorkabelService
from sqlalchemy import select
from sqlalchemy.orm import Session
from utils.excel_reader import (
    DesignMetaData,
    ExcelReader,
    ExcelReaderResult,
    ExistingMetaData,
)


# --- The Logic Layer (Service) ---
class UploadService:
    def __init__(self, db: Session):
        self.db = db

    def run(self, excel_file: ExcelReaderResult):
        try:
            processed_data = ExcelReader(excel_file).render()[0]
            user = self._get_user(id=1)
            upload = self._add_upload(user)
            tekening = self._add_tekening(upload, metadata=processed_data.metadata)
            versie_bestaand, _ = self._add_versie(
                tekening,
                metadata=processed_data.metadata,
                metadata_new=processed_data.metadata_new,
            )
            self._add_gils(tekening)
            self._add_spoorkabels(versie_bestaand, records=processed_data.records)
            self.db.commit()

            return {
                "geocodenaam": processed_data.metadata.geocodenaam,
                "discipline": tekening.discipline,
            }

        except Exception as e:
            self.db.rollback()
            logger.error("Upload rolled back due to error: ", e)
            # TODO: Add return for error
            pass

    def _get_user(self, id: int = 1) -> User:
        user = self.db.scalars(select(User).where(User.id == id)).first()
        if not user:
            raise ValueError(f"User {user} not found")
        return user

    def _add_upload(self, user: User) -> Upload:
        upload = Upload(user_id=user.id)
        self.db.add(upload)
        self.db.flush()
        return upload

    def _add_tekening(self, upload: Upload, metadata: ExistingMetaData) -> Tekening:
        tekeningnaam = metadata.gil

        stmt = select(Tekening).where(Tekening.naam == tekeningnaam)
        tekening = self.db.scalars(stmt).first()

        if not tekening:
            tekening = Tekening(
                upload_id=upload.id,
                naam=metadata.gil,
                geocodenaam=metadata.geocodenaam,
                regio=metadata.gebied,
            )
            self.db.add(tekening)
            self.db.flush()

        return tekening

    def _add_versie(
        self,
        tekening: Tekening,
        metadata: ExistingMetaData,
        metadata_new: DesignMetaData | None,
    ) -> tuple[VersieBestaand, VersieOntwerp | None]:
        stmt = select(Versie).where(Versie.tekening_id == tekening.id)
        versie = self.db.scalars(stmt).first()
        versie_code = metadata.versie

        if not versie:
            versie_bestaand = VersieBestaand(
                tekening_id=tekening.id,
                versie_code=versie_code,
                aantal_regels=metadata.aantal_regels,
                hoogste_gil=metadata.hoogste_gil,
                is_reversed_engineerd=metadata.is_reversed_engineerd,
            )
            self.db.add(versie_bestaand)
            self.db.flush()

        if versie:
            stmt = select(VersieBestaand).where(
                VersieBestaand.tekening_id == versie.tekening_id,
                VersieBestaand.versie_code == versie_code,
            )

            versie_bestaand = self.db.scalars(stmt).first()

        self.versie_bestaand = versie_bestaand

        if metadata_new:
            versie_ontwerp = self._add_versie_ontwerp(
                versie_bestaand, tekening=tekening, metadata_new=metadata_new
            )
        else:
            versie_ontwerp = None

        return [versie_bestaand, versie_ontwerp]

    def _add_versie_ontwerp(
        self,
        versie_bestaand: VersieBestaand,
        tekening: Tekening,
        metadata_new: DesignMetaData,
    ):
        # TODO: Add ontwerp fase to this function

        versie_ini_code = metadata_new.versie_ini

        stmt = select(VersieOntwerp).where(
            VersieOntwerp.id == versie_bestaand.id,
            VersieOntwerp.versie_ini == versie_ini_code,
        )
        versie_ontwerp = self.db.scalars(stmt).first()

        if not versie_ontwerp:
            versie_ontwerp = VersieOntwerp(
                tekening_id=tekening.id,
                versie_ini=versie_ini_code,
                parent_versie_bestaand_id=versie_bestaand.id,
            )

            self.db.add(versie_ontwerp)
            self.db.flush()

        return versie_ontwerp

    def _order_fases(self, metadata_new: DesignMetaData) -> dict[str, dict]:
        ab = {k: v for k, v in asdict(metadata_new).items() if "ab" in k}
        rr = {k: v for k, v in asdict(metadata_new).items() if "rr" in k}
        tb = {k: v for k, v in asdict(metadata_new).items() if "tb" in k}

        return {"ab": ab, "rr": rr, "tb": tb}

    def _add_versie_ontwerp_fase(
        self, versie_ontwerp: VersieOntwerp, metadata_new: DesignMetaData
    ):
        fases = self._order_fases(metadata_new)

        results = []
        for key, fase in fases.items():
            _versie = fase.get(f"versie_{key}")
            _aantal_regels = fase.get(f"aantal regels_{key}")
            _prorail_projectnr = fase.get(f"prorail_projectnr_{key}")
            _hoogste_gil = fase.get(f"hoogste_gil_{key}")

            stmt = select(VersieOntwerpFase).where(
                VersieOntwerpFase.versie_ontwerp_id == versie_ontwerp.id,
                VersieOntwerpFase.fase_code == key,
            )
            versie_ontwerp_fase = self.db.scalars(stmt).first()

            if not versie_ontwerp_fase:
                versie_ontwerp_fase = VersieOntwerpFase(
                    versie_ontwerp_id=versie_ontwerp.id,
                    fase_code=key,
                    versie_code=_versie,
                    aantal_regels=_aantal_regels,
                    hoogste_gil=_hoogste_gil,
                    prorail_projectnr=_prorail_projectnr,
                )

                self.db.add(versie_ontwerp_fase)
                self.db.flush()
                results.append(versie_ontwerp_fase)

        return results

    def _add_gils(self, tekening: Tekening):
        prorail_service = ProrailFeatureService(db=self.db)
        result = prorail_service.sync_features_by_tekening(tekening)
        return result

    def _add_spoorkabels(
        self, versie_bestaand: VersieBestaand, records: list[SpoorkabelCreate]
    ):
        service = SpoorkabelService(
            db=self.db,
            spoorkabel_schemas=records,
            versie=versie_bestaand,
        )
        service.insert_spoorkabel()
        service.insert_relates()


if __name__ == "__main__":
    from core.config import test_files
    from core.database import get_db

    db = next(get_db())

    uploader = UploadService(db=db)

    for index, file in enumerate(test_files.valid_excel_files[101:], start=1):
        print(f"Currently at: {index}")
        uploader.run(excel_file=file)
