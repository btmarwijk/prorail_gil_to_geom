from models.versie_model import VersieBestaand, VersieOntwerp, VersieOntwerpFase
from sqlalchemy.orm import Session
from utils.excel_reader import DesignMetaData, ExistingMetaData


class VersieService:
    def __init__(self, db_session: Session):
        self.db = db_session

    def process_metadata(
        self, tekening_id: int, metadata_obj: ExistingMetaData | DesignMetaData
    ):
        """
        Bepaalt welk type versie geladen moet worden en voert de mapping uit.
        """
        if isinstance(metadata_obj, ExistingMetaData):
            return self._load_existing(tekening_id, metadata_obj)
        elif isinstance(metadata_obj, DesignMetaData):
            return self._load_design(tekening_id, metadata_obj)

    def _load_existing(self, tekening_id: int, data: ExistingMetaData):
        # Directe mapping naar de ExistingVersie tabel
        existing = VersieBestaand(
            tekening_id=tekening_id,
            gil=data.gil,
            geocodenaam=data.geocodenaam,
            gedownload=data.gedownload,
            gebied=data.gebied,
            versie_nummer=data.versie,
            aantal_regels=data.aantal_regels,
            hoogste_gil=data.hoogste_gil,
        )
        self.db.add(existing)
        return existing

    def _load_design(self, tekening_id: int, data: DesignMetaData):
        # 1. Maak de hoofdeniteit aan
        design = VersieOntwerp(
            tekening_id=tekening_id,
            gil=data.gil,
            geocodenaam=data.geocodenaam,
            gedownload=data.gedownload,
            regio=data.regio,
            # parent_existing_versie_id kan hier later worden toegevoegd
        )

        # 2. De "Ontvouw"-logica voor de fasen (INI, AB, RR, TB)
        # We mappen de kolommen uit de Excel naar rijen in de DesignPhase tabel
        phase_map = [
            (
                "INI",
                data.versie_ini,
                data.aantal_regels_ini,
                data.hoogste_gil_ini,
                None,
            ),
            (
                "AB",
                data.versie_ab,
                data.aantal_regels_ab,
                data.hoogste_gil_ab,
                data.prorail_projectnr_ab,
            ),
            (
                "RR",
                data.versie_rr,
                data.aantal_regels_rr,
                data.hoogste_gil_rr,
                data.prorail_projectnr_rr,
            ),
            (
                "TB",
                data.versie_tb,
                data.aantal_regels_tb,
                data.hoogste_gil_tb,
                data.prorail_projectnr_tb,
            ),
        ]

        for code, versie, regels, hoogste, proj_nr in phase_map:
            if versie:  # Alleen toevoegen als de fase daadwerkelijk data bevat
                phase = VersieOntwerpFase(
                    phase_code=code,
                    versie_code=versie,
                    aantal_regels=regels or 0,
                    hoogste_gil=hoogste or 0,
                    prorail_projectnr=proj_nr,
                )
                design.phases.append(phase)

        self.db.add(design)
        return design
