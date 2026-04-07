from pathlib import Path

from dotenv import dotenv_values
from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

config = dotenv_values()


class Settings(BaseSettings):
    # The attributes must match your .env keys (case-insensitive by default)
    db_user: str = config.get("DB_USER")
    db_password: str = config.get("DB_PASSWORD")
    db_name: str = config.get("DB_NAME")
    db_host: str = config.get("DB_HOST")
    db_port: int = config.get("DB_PORT")

    # PostGIS specific settings if needed
    debug: bool = False

    # Pydantic v2 configuration for reading the .env file
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",  # Ignores extra variables in .env not defined here
    )

    @property
    def database_url(self) -> str:
        """Helper to generate the connection string."""
        return f"postgresql://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"


class TestFiles(BaseModel):
    BASE_DIR: Path = Path(__file__).resolve().parent.parent.parent
    DATA_DIR: Path = BASE_DIR / "data"

    INPUT_DIR: Path = DATA_DIR / "input"

    # The minimal file you want to run first (Small section of the Maasvlakte)
    SMALL_SINGLE_FILE: Path = INPUT_DIR / "publiceer.xlsx"

    # Two files from a relative minor railway station
    ALPHEN_FILE_1: Path = INPUT_DIR / "623KS01.xlsx"
    ALPHEN_FILE_2: Path = INPUT_DIR / "623KS02.xlsx"

    # A single tekeningnaam (560KS01), but a big train station (Den Haag Centraal)
    SINGLE_KABEL_FILE: Path = INPUT_DIR / "R-537600-KeL-UO300-LST-001.xlsx"

    # A multi-sheet excel-file for the maasvlakte (Rotterdam port)
    MULTI_KABEL_FILE: Path = INPUT_DIR / "GIL A+B.xlsx"
    RAW_GIL_FILE: Path = INPUT_DIR / "560KS01.xlsx"

    DEN_HAAG_FILE_1_KS: Path = INPUT_DIR / "536KS01.xlsx"

    DEN_HAAG_FILE_2_KS: Path = INPUT_DIR / "561KS01.xlsx"

    # These are all the kabels & leidingen for 1 tekeningnaam
    DEN_HAAG_FILE_3_KS: Path = INPUT_DIR / "564KS01.xlsx"
    DEN_HAAG_FILE_3_WV: Path = INPUT_DIR / "564WV01.xlsx"
    DEN_HAAG_FILE_3_WB: Path = INPUT_DIR / "564WB01.xlsx"
    DEN_HAAG_FILE_3_RD: Path = INPUT_DIR / "564RD01.xlsx"


# Instantiate the settings object to be imported elsewhere
settings = Settings()
test_files = TestFiles()

if __name__ == "__main__":
    print(settings)
