import warnings
from dataclasses import dataclass
from io import BytesIO
from typing import Any, Literal, Tuple

import numpy as np
import openpyxl
import pandas as pd
from core import logger
from core.config import test_files
from schemas.spoorkabel_schema import SpoorkabelCreate
from utils.versie_subtract import decrement_string

warnings.filterwarnings("ignore", category=UserWarning, module="openpyxl")


@dataclass
class ExistingMetaData:
    gil: str
    gebied: str
    versie: str
    aantal_regels: int
    geocodenaam: str
    gedownload: str
    hoogste_gil: int
    is_reversed_engineerd: bool = False


@dataclass
class DesignMetaData:
    gil: str
    regio: str
    versie_ini: str
    aantal_regels_ini: int
    geocodenaam: str
    gedownload: str
    hoogste_gil_ini: int

    versie_ab: str | None = None
    versie_rr: str | None = None
    versie_tb: str | None = None

    aantal_regels_ab: int | None = None
    aantal_regels_rr: int | None = None
    aantal_regels_tb: int | None = None

    prorail_projectnr_ab: str | None = None
    prorail_projectnr_rr: str | None = None
    prorail_projectnr_tb: str | None = None

    hoogste_gil_ab: int | None = None
    hoogste_gil_rr: int | None = None
    hoogste_gil_tb: int | None = None


@dataclass
class ExcelFileReaderResult:
    metadata: Any
    dataframe: pd.DataFrame
    new_tekening: bool

    class Config:
        arbitrary_types_allowed = True


class ExcelFileReaderResponse:
    results: list[ExcelFileReaderResult]


class ExcelFileReader:
    def __init__(self, file_source: str | BytesIO):
        self.file_source = file_source
        self._new_tekening = False

    def _excel_file(self) -> openpyxl.Workbook:
        # Als file_source een BytesIO object is, zorg dat de pointer op 0 staat
        if isinstance(self.file_source, bytes):
            self.file_source = BytesIO(self.file_source)

        # load_workbook accepteert zowel een pad (string) als een BytesIO object
        return openpyxl.load_workbook(self.file_source, data_only=True)

    def _find_header_row(self, ws) -> int:
        target_columns = {"KABELNUMMER", "KABEL_GEBOREN"}
        for row in ws.iter_rows(values_only=False):
            for cell in row:
                if cell.value in target_columns:
                    return cell.row
        return None

    def read_sheets(self):
        wb = self._excel_file()
        results = []
        for ws in wb.worksheets:
            if ws.cell(row=2, column=3).value == "VERSIE_AB:":
                self._new_tekening = True

            header_row_num = self._find_header_row(ws)

            if header_row_num:
                # 1. Convert all worksheet values to a list of lists
                # openpyxl is 1-indexed, so row 5 is index 4 in a list
                all_data = list(ws.values)
                header_idx = header_row_num - 1

                # 2. Extract metadata (everything above the header)
                metadata = all_data[:header_idx]

                # 3. Extract DataFrame data (header row + everything below)
                df_data = all_data[header_idx:]

                # Create DataFrame using the first row of df_data as columns
                df = pd.DataFrame(df_data[1:], columns=df_data[0])

            else:
                print(f"Target headers not found in sheet: {ws.title}")

            results.append(
                ExcelFileReaderResult(
                    metadata=metadata, dataframe=df, new_tekening=self._new_tekening
                )
            )

        return results


class ExcelMetaDataReader:
    def __init__(self, raw_data: ExcelFileReaderResult):
        self.raw_data = raw_data

    def _get_value_by_label(self, label_item: str) -> Any:
        """
        Searches for label_item in a 2D list/tuple structure
        and returns the value from the next index.
        """
        # Ensure we match the colon if the user didn't provide it
        if not label_item.endswith(":"):
            label_item += ":"

        for row in self.raw_data.metadata:
            for index, item in enumerate(row):
                if item == label_item:
                    # Ensure there is an index after the label
                    if index + 1 < len(row):
                        return row[index + 1]
        return None

    def _get_metadata_existing(self):
        gebied = self._get_value_by_label("GEBIED:")
        regio = self._get_value_by_label("REGIO:")

        gebied_input = gebied or regio

        metadata = ExistingMetaData(
            gil=self._get_value_by_label("GIL:"),
            gebied=gebied_input,
            versie=self._get_value_by_label("VERSIE:"),
            aantal_regels=self._get_value_by_label("AANTAL_REGELS:"),
            geocodenaam=self._get_value_by_label("GEOCODENAAM:"),
            gedownload=self._get_value_by_label("GEDOWNLOAD:"),
            hoogste_gil=self._get_value_by_label("HOOGSTE_GIL:"),
        )

        return metadata

    def _get_metadata_design(self):
        gebied = self._get_value_by_label("GEBIED:")
        regio = self._get_value_by_label("REGIO:")

        gebied_input = gebied or regio

        _versie1 = self._get_value_by_label("VERSIE_INI:")
        _versie2 = self._get_value_by_label("VERSIE:")

        versie = _versie1 or _versie2

        versie_subtracted = decrement_string(versie)

        metadata = ExistingMetaData(
            gil=self._get_value_by_label("GIL:"),
            gebied=gebied_input,
            versie=versie_subtracted,
            aantal_regels=self._get_value_by_label("AANTAL_REGELS:") or None,
            geocodenaam=self._get_value_by_label("GEOCODENAAM:") or None,
            gedownload=self._get_value_by_label("GEDOWNLOAD:") or None,
            hoogste_gil=self._get_value_by_label("HOOGSTE_GIL:") or None,
            is_reversed_engineerd=True,
        )

        metadata_new = DesignMetaData(
            gil=self._get_value_by_label("GIL:"),
            regio=self._get_value_by_label("REGIO:"),
            versie_ini=versie,
            versie_ab=self._get_value_by_label("VERSIE_AB:"),
            versie_rr=self._get_value_by_label("VERSIE_RR:"),
            versie_tb=self._get_value_by_label("VERSIE_TB:"),
            aantal_regels_ini=int(
                self._get_value_by_label("AANTAL REGELS_INI:") or None
            ),
            aantal_regels_ab=self._get_value_by_label("AANTAL REGELS_AB:"),
            aantal_regels_rr=self._get_value_by_label("AANTAL REGELS_RR:"),
            aantal_regels_tb=self._get_value_by_label("AANTAL REGELS_TB:"),
            geocodenaam=self._get_value_by_label("GEOCODENAAM:"),
            prorail_projectnr_ab=self._get_value_by_label("PRORAIL PROJECTNR_AB:"),
            prorail_projectnr_rr=self._get_value_by_label("PRORAIL PROJECTNR_RR:"),
            prorail_projectnr_tb=self._get_value_by_label("PRORAIL PROJECTNR_TB:"),
            gedownload=self._get_value_by_label("GEDOWNLOAD:"),
            hoogste_gil_ini=self._get_value_by_label("HOOGSTE GIL_INI:"),
            hoogste_gil_ab=self._get_value_by_label("HOOGSTE GIL_AB:"),
            hoogste_gil_rr=self._get_value_by_label("HOOGSTE GIL_RR:"),
            hoogste_gil_tb=self._get_value_by_label("HOOGSTE GIL_TB:"),
        )

        return metadata, metadata_new

    def get_metadata(self) -> Tuple[Tuple[list], Tuple[list] | None]:
        if self.raw_data.new_tekening:
            # Design metadata
            metadata, metadata_new = self._get_metadata_design()
            return (metadata, metadata_new)

        # Existing metadata
        metadata = self._get_metadata_existing()
        return (metadata, None)


class ExcelSheetReader:
    def __init__(
        self,
        raw_data: ExcelFileReaderResult,
        remove_empty_geulen: bool = True,
        remove_duplicate_geulen: bool = False,
    ) -> None:
        self._df = raw_data.dataframe
        self.remove_empty_geulen = remove_empty_geulen
        self.remove_duplicate_geulen = remove_duplicate_geulen
        self._new_tekening: bool = raw_data.new_tekening
        self._render()

    def _split_new_old(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
        if self._new_tekening:
            df_old = df[df["OUD/NIEUW"] == "OUD"]
            df_new = df[df["OUD/NIEUW"] == "NIEUW"]
            return df_old, df_new

        return df, None

    def _filter_rows(
        self,
        df: pd.DataFrame,
    ) -> pd.DataFrame:
        self._raw_shape = df.shape

        df_without_empty = df.dropna(subset=["KABELNUMMER", "GEULEN"])
        self._shape_without_empty = df_without_empty.shape
        df_without_duplicates = df_without_empty.drop_duplicates(subset=["GEULEN"])
        self._shape_without_duplicates = df_without_duplicates.shape

        if self.remove_empty_geulen and self.remove_duplicate_geulen:
            return df_without_duplicates

        if self.remove_empty_geulen and not self.remove_duplicate_geulen:
            return df_without_empty

        if not self.remove_empty_geulen and self.remove_duplicate_geulen:
            raise ValueError("You cannot remove duplicate geulen but keep empty ones")

        return df

    def _render(self) -> None:
        logger.info("Reading the prorail excel-file...")

        df = self._df
        df = df.replace("", None)
        df = df.dropna(axis=1, how="all")

        self._raw_shape = df.shape
        self.table: pd.DataFrame = (
            self._filter_rows(df=df).reset_index(drop=True).replace({np.nan: None})
        )

    def to_pydantic_create(
        self,
    ) -> Tuple[list[SpoorkabelCreate], list[SpoorkabelCreate] | None]:
        if self._new_tekening:
            df_old, df_new = self._split_new_old(self.table)
            records = df_old.to_dict(orient="records")
            records_new = df_new.to_dict(orient="records")
            parsed = [SpoorkabelCreate(**record) for record in records]
            parsed_new = [SpoorkabelCreate(**record) for record in records_new]
            return (parsed, parsed_new)

        df_old, _ = self._split_new_old(self.table)
        records = df_old.to_dict(orient="records")

        return ([SpoorkabelCreate(**record) for record in records], None)


@dataclass
class ExcelReaderResult:
    type: Literal["bestaand", "ontwerp"]
    metadata: ExistingMetaData
    metadata_new: DesignMetaData | None
    records: list[SpoorkabelCreate]
    records_new: list[SpoorkabelCreate] | None


class ExcelReader:
    def __init__(self, file_source: str):
        self.file_reader = ExcelFileReader(file_source=file_source)
        self.results = []

    def render(self) -> list[ExcelReaderResult]:
        """
        Orchestrates the reading, metadata extraction,
        and table conversion for all sheets.
        """
        # 1. Get the raw data from the file
        raw_sheets = self.file_reader.read_sheets()

        for sheet in raw_sheets:
            # 2. Extract Metadata
            # (Assuming sheet is the dict/object returned by your FileReader)
            metadata, metadata_new = ExcelMetaDataReader(raw_data=sheet).get_metadata()

            if metadata_new:
                type = "ontwerp"
            else:
                type = "bestaand"

            # 3. Convert Table data to Pydantic models
            records = ExcelSheetReader(raw_data=sheet).to_pydantic_create()[0]
            records_new = ExcelSheetReader(raw_data=sheet).to_pydantic_create()[1]

            # 4. Store the combined result
            self.results.append(
                ExcelReaderResult(
                    **{
                        "type": type,
                        "metadata": metadata,
                        "metadata_new": metadata_new if metadata_new else None,
                        "records": records,
                        "records_new": records_new if records_new else None,
                    }
                )
            )

        return self.results


if __name__ == "__main__":
    input_files = [test_files.SMALL_SINGLE_FILE]

    for file in input_files:
        reader = ExcelReader(file_source=file)
        processed_data = reader.render()

        print(processed_data[0].metadata)
        print(processed_data[0].metadata_new)
