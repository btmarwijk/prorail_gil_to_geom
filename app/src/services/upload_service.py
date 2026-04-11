import io

import pandas as pd
from utils.excel_reader import ExcelReader


# --- The Logic Layer (Service) ---
class UploadProcessor:
    def __init__(self, preview_rows: int = 5):
        self.preview_rows = preview_rows

    def process(self, file_bytes: bytes) -> pd.DataFrame:
        return ExcelReader(io.BytesIO(file_bytes))
