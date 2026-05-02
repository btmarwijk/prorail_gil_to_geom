from pathlib import Path

from dotenv import dotenv_values
from pydantic import BaseModel, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict

config = dotenv_values()


class Settings(BaseSettings):
    # The attributes must match your .env keys (case-insensitive by default)
    db_user: str = config.get("DB_USER")
    db_password: str = config.get("DB_PASSWORD")
    db_name: str = config.get("DB_NAME")
    db_host: str = config.get("DB_HOST")
    db_port: int = config.get("DB_PORT")

    REDIS_PASSWORD: str = config.get("REDIS_PASSWORD")
    CELERY_BROKER_URL: str = f"redis://:{REDIS_PASSWORD}@redis:6379/0"
    CELERY_RESULT_BACKEND: str = f"redis://:{REDIS_PASSWORD}@redis:6379/1"
    # PostGIS specific settings if needed
    debug: bool = False

    # Pydantic v2 configuration for reading the .env file
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",  # Ignores extra variables in .env not defined here
    )

    PRORAIL_FEATURE_SERVER_KS: str = (
        "https://maps.prorail.nl/arcgis/rest/services/Kabelsituatie/FeatureServer"
    )
    PRORAIL_FEATURE_SERVER_WV: str = "https://maps.prorail.nl/arcgis/rest/services/Wisselverwarming_en_Gas/FeatureServer"
    PRORAIL_FEATURE_SERVER_WB: str = "https://maps.prorail.nl/arcgis/rest/services/Water__en_Brandleidingen/FeatureServer"
    PRORAIL_FEATURE_SERVER_RD: str = "https://maps.prorail.nl/arcgis/rest/services/Riool__Drainage_en_Diesel/FeatureServer"

    @property
    def database_url(self) -> str:
        """Helper to generate the connection string."""
        return f"postgresql://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"


class TestFiles(BaseModel):
    BASE_DIR: Path = Path(__file__).resolve().parent.parent.parent
    DATA_DIR: Path = BASE_DIR / "data"

    INPUT_DIR: Path = DATA_DIR / "input"
    EXCELS_DIR: Path = DATA_DIR / "Excels"
    VALID_EXCELS_DIR: Path = DATA_DIR / "output" / "valid_file"

    @computed_field
    @property
    def excel_files(self) -> list[Path]:
        # This handles both .xlsx and .xls
        return list(self.EXCELS_DIR.glob("*.xls*"))

    @computed_field
    @property
    def valid_excel_files(self) -> list[Path]:
        # This handles both .xlsx and .xls
        return sorted(self.VALID_EXCELS_DIR.glob("*.xls*"))


# Instantiate the settings object to be imported elsewhere
settings = Settings()
test_files = TestFiles()

if __name__ == "__main__":
    print(test_files.valid_excel_files[:4])
