from dataclasses import asdict

import pandas as pd
from core.database import SessionLocal
from models import (
    Tekening,
    Upload,
    User,
    Versie,
    VersieBestaand,
    VersieOntwerp,
    VersieOntwerpFase,
)
from services.prorail_gil_service import ProrailFeatureService
from services.spoorkabel_service import SpoorkabelService
from sqlalchemy import select
from utils.excel_reader import ExcelReader, ExcelReaderResult


# --- The Logic Layer (Service) ---
class UploadService:
    def __init__(self):
        self.db = SessionLocal()

    def get_user_by_id(self, id: int = 1) -> None:
        user = self.db.scalars(select(User).where(User.id == 1)).first()
        if not user:
            raise ValueError(f"User {user} not found")
        self.user = user

    def process(self, excel_file) -> pd.DataFrame:
        return ExcelReader(excel_file).render()

    def process_manual(self, excel_file: ExcelReaderResult):
        self.processed_excel = ExcelReader(excel_file).render()[0]

    def _add_upload(self):
        upload = Upload(user_id=self.user.id)
        self.db.add(upload)
        self.db.commit()
        self.upload = upload
        return upload

    def _add_tekening(self):
        tekeningnaam = self.processed_excel.metadata.gil

        stmt = select(Tekening).where(Tekening.naam == tekeningnaam)
        tekening = self.db.scalars(stmt).first()

        if not tekening:
            tekening = Tekening(
                upload_id=self.upload.id,
                naam=self.processed_excel.metadata.gil,
                geocodenaam=self.processed_excel.metadata.geocodenaam,
                regio=self.processed_excel.metadata.gebied,
            )
            self.db.add(tekening)
            self.db.commit()
            self.db.refresh(tekening)

        self.tekening = tekening
        return tekening

    def _add_versie(self):
        stmt = select(Versie).where(Versie.tekening_id == self.tekening.id)
        versie = self.db.scalars(stmt).first()
        versie_code = self.processed_excel.metadata.versie

        if not versie:
            versie_bestaand = VersieBestaand(
                tekening_id=self.tekening.id,
                versie_code=versie_code,
                aantal_regels=self.processed_excel.metadata.aantal_regels,
                hoogste_gil=self.processed_excel.metadata.hoogste_gil,
                is_reversed_engineerd=self.processed_excel.metadata.is_reversed_engineerd,
            )
            self.db.add(versie_bestaand)
            self.db.commit()

        if versie:
            stmt = select(VersieBestaand).where(
                VersieBestaand.tekening_id == versie.tekening_id,
                VersieBestaand.versie_code == versie_code,
            )

            versie_bestaand = self.db.scalars(stmt).first()

        self.versie_bestaand = versie_bestaand

        if self.processed_excel.type == "ontwerp":
            versie_ontwerp = self._add_versie_ontwerp(versie_bestaand)
        else:
            versie_ontwerp = None

        return [versie_bestaand, versie_ontwerp]

    def _add_versie_ontwerp(self, versie_bestaand: VersieBestaand):
        # TODO: Add ontwerp fase to this function

        versie_ini_code = self.processed_excel.metadata_new.versie_ini

        stmt = select(VersieOntwerp).where(
            VersieOntwerp.id == versie_bestaand.id,
            VersieOntwerp.versie_ini == versie_ini_code,
        )
        versie_ontwerp = self.db.scalars(stmt).first()

        if not versie_ontwerp:
            versie_ontwerp = VersieOntwerp(
                tekening_id=self.tekening.id,
                versie_ini=versie_ini_code,
                parent_versie_bestaand_id=versie_bestaand.id,
            )

            self.db.add(versie_ontwerp)
            self.db.commit()

        return versie_ontwerp

    def _order_fases(self) -> dict[str, dict]:
        metadata_new = self.processed_excel.metadata_new
        ab = {k: v for k, v in asdict(metadata_new).items() if "ab" in k}
        rr = {k: v for k, v in asdict(metadata_new).items() if "rr" in k}
        tb = {k: v for k, v in asdict(metadata_new).items() if "tb" in k}

        return {"ab": ab, "rr": rr, "tb": tb}

    def _add_versie_ontwerp_fase(self, versie_ontwerp: VersieOntwerp):
        fases = self._order_fases()

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
                self.db.commit()
                results.append(versie_ontwerp_fase)

        return results

    def _add_gils(self):
        prorail_service = ProrailFeatureService(db=self.db)
        return prorail_service.sync_features_by_tekening(
            self.tekening.id, tekeningnaam=self.tekening.naam
        )

    def _add_spoorkabels(self):
        service = SpoorkabelService(
            spoorkabel_schemas=self.processed_excel.records, versie=self.versie_bestaand
        )
        service.insert_spoorkabel()
        service.insert_relates()


if __name__ == "__main__":
    from core.config import test_files

    uploader = UploadService()
    uploader.get_user_by_id()

    for index, file in enumerate(test_files.valid_excel_files[1::15]):
        try:
            print(f"{index}: {file}")
            uploader.process_manual(excel_file=file)
            upload = uploader._add_upload()
            tekening = uploader._add_tekening()
            versie = uploader._add_versie()
            uploader._add_gils()
            uploader._add_spoorkabels()
        except Exception as e:
            raise e
