import warnings

import numpy as np
import openpyxl
import pandas as pd

from core import logger, settings, test_files
from schemas.meta_spoorkabel_schema import MetaSpoorkabelCreate, MetaSpoorkabelRead

warnings.filterwarnings("ignore", category=UserWarning, module="openpyxl")
# --- All Column names ---
# ['OUD/NIEUW', 'KABELNUMMER', 'KABEL_GEBOREN', 'KABELNAAM',
# 'KABELNAAM_OUD', 'VAN', 'NAAR', 'KABELTYPE', 'GROEP', 'SUB_GROEP',
# 'VAN_GIL', 'NAAR_GIL', 'OPMERKING', 'GEULEN', 'MAX_LENGTE', 'TB_LENGTE',
# 'AB_LENGTE', 'REGELNUMMER']


class ExcelReader:
    """
    A utility class to read, filter, and transform ProRail Excel files containing cable data.

    This class handles the extraction of metadata (tekeningnaam, geocodenaam, gedownload (datetime)),
    identifies the header row dynamically, and provides methods to export the
    data to DataFrames, Pydantic models, or ArcGIS services.
    """

    def __init__(
        self,
        file_path: str,
        remove_empty_geulen: bool = True,
        remove_duplicate_geulen: bool = False,
    ) -> None:
        self.file_path = file_path
        self.remove_empty_geulen = remove_empty_geulen
        self.remove_duplicate_geulen = remove_duplicate_geulen
        self.tekeningnamen = []
        self._render()

    def __repr__(self) -> str:
        return (
            f"<ExcelFile Shape_raw={self._raw_shape}, "
            f"Shape_withouth_empty={self._shape_without_empty}, "
            f"Shape_withouty_duplicates={self._shape_without_duplicates}, "
            f"Tekeningnamen={self.tekeningnamen}, "
            f"Header_row=({self._header_row}) />"
        )

    @property
    def tekeningnamen_str(self) -> str:
        return ", ".join(f"'{n}'" for n in self.tekeningnamen)

    def get_tekeningnamen_str(self) -> str:
        """Returns a comma-separated string of drawing names wrapped in single quotes."""
        return ", ".join(f"'{n}'" for n in self.tekeningnamen)

    @property
    def excel_file(self) -> openpyxl.Workbook:
        return openpyxl.load_workbook(self.file_path, data_only=True)

    @property
    def _sheet_names(self) -> list[str]:
        return self.excel_file.sheetnames

    @property
    def _has_multiple_sheets(self) -> bool:
        if len(self._sheet_names) == 1:
            return False
        if len(self._sheet_names) > 1:
            return True

    def _get_cell_value_by_label(self, sheet_name: str, label_cell: str, value_cell: str, expected_label: str) -> str:
        """
        Generic helper to validate a label and return the corresponding value from an Excel sheet.
        """
        ws = self.excel_file[sheet_name]
        label_val = ws[label_cell].value
        value_val = ws[value_cell].value

        if label_val != expected_label:
            raise ValueError(f"Expected '{expected_label}' in cell {label_cell}")

        if value_val is None:
            raise ValueError(f"Cell {value_cell} is empty. {expected_label} is required.")

        return value_val

    def _find_header_row(self, sheet_name: str) -> int:
        ws = self.excel_file[sheet_name]
        target_columns = {"KABELNUMMER", "KABEL_GEBOREN"}
        for row in ws.iter_rows(values_only=False):
            for cell in row:
                if cell.value in target_columns:
                    return cell.row

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

    def _read_single_sheet(self, sheet_name: str | None = None) -> pd.DataFrame:
        # Metadata on the input table added as column
        tekeningnaam = self._get_cell_value_by_label(
            sheet_name=sheet_name, label_cell="A1", value_cell="B1", expected_label="GIL:"
        )
        self.versie = self._get_cell_value_by_label(
            sheet_name=sheet_name, label_cell="C1", value_cell="D1", expected_label="VERSIE:"
        )
        self.geocodenaam = self._get_cell_value_by_label(
            sheet_name=sheet_name, label_cell="G1", value_cell="H1", expected_label="GEOCODENAAM:"
        )
        self.gedownload = self._get_cell_value_by_label(
            sheet_name=sheet_name, label_cell="I1", value_cell="J1", expected_label="GEDOWNLOAD:"
        )

        # header_row is the index of the row containing the column names
        self._header_row = self._find_header_row(sheet_name=sheet_name)

        df: pd.DataFrame = pd.read_excel(
            self.file_path,
            sheet_name=sheet_name,
            skiprows=self._header_row - 1,
        )

        df["tekeningnaam"] = tekeningnaam
        self.tekeningnamen.append(tekeningnaam)

        df["geocodenaam"] = self.geocodenaam
        df["gedownload"] = self.gedownload
        df["versie"] = self.versie
        return df

    def _read_multiple_sheets(self) -> pd.DataFrame:
        dfs = []
        for sheet_name in self._sheet_names:
            _df = self._read_single_sheet(sheet_name=sheet_name)
            dfs.append(_df)

        return pd.concat(dfs, ignore_index=True)

    def _render(self) -> None:
        logger.info("Reading the prorail excel-file...")

        df = (
            self._read_multiple_sheets()
            if self._has_multiple_sheets
            else self._read_single_sheet(sheet_name=self._sheet_names[0])
        )
        self._raw_shape = df.shape
        self.table: pd.DataFrame = self._filter_rows(df=df).reset_index(drop=True).replace({np.nan: None})

    def to_dict(self) -> list[dict]:
        return self.table.to_dict(orient="records")

    def to_pydantic_create(self) -> list[MetaSpoorkabelCreate]:
        records = self.to_dict()
        return [MetaSpoorkabelCreate(upload_guid=None, **record) for record in records]



if __name__ == "__main__":
    reader = ExcelReader(
        file_path=test_files.SINGLE_KABEL_FILE, remove_empty_geulen=True, remove_duplicate_geulen=False
    )
    results: list[MetaSpoorkabelCreate] = reader.to_pydantic_create()
    print(results[10].model_dump(by_alias=True))