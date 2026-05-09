import secrets
from pathlib import Path
from typing import Literal

from dotenv import dotenv_values
from pydantic import BaseModel, EmailStr, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict

config = dotenv_values()


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",  # Ignores extra variables in .env not defined here
    )
    PROJECT_NAME: str = "DigiLayer"
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    # 60 minutes * 24 hours * 8 days = 8 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    FRONTEND_HOST: str = "http://localhost:5173"
    ENVIRONMENT: Literal["local", "staging", "production"] = "local"

    # Postgres/PostGIS
    DB_USER: str = config.get("DB_USER")
    DB_PASSWORD: str = config.get("DB_PASSWORD")
    DB_NAME: str = config.get("DB_NAME")
    DB_HOST: str = config.get("DB_HOST")
    DB_PORT: int = config.get("DB_PORT")

    # Redis/Caching
    REDIS_PASSWORD: str = config.get("REDIS_PASSWORD")

    # Celery/Task Management
    CELERY_BROKER_URL: str = f"redis://:{REDIS_PASSWORD}@redis:6379/0"
    CELERY_RESULT_BACKEND: str = f"redis://:{REDIS_PASSWORD}@redis:6379/1"

    # Email/SMTP
    SMTP_TLS: bool = True
    SMTP_SSL: bool = False
    SMTP_HOST: str = config.get("SMTP_SERVER")
    SMTP_PORT: int = config.get("SMTP_PORT")
    SMTP_USER: str = config.get("EMAIL_USERNAME")
    SMTP_PASSWORD: str = config.get("EMAIL_PASSWORD")

    EMAILS_FROM_EMAIL: EmailStr | None = "test@digilayer.com"
    EMAILS_FROM_NAME: str | None = "Boudewijn"
    EMAIL_TEST_USER: EmailStr = "test@digilayer.com"

    EMAIL_RESET_TOKEN_EXPIRE_HOURS: int = 48

    # Prorail GIS urls
    PRORAIL_FEATURE_SERVER_KS: str = (
        "https://maps.prorail.nl/arcgis/rest/services/Kabelsituatie/FeatureServer"
    )
    PRORAIL_FEATURE_SERVER_WV: str = "https://maps.prorail.nl/arcgis/rest/services/Wisselverwarming_en_Gas/FeatureServer"
    PRORAIL_FEATURE_SERVER_WB: str = "https://maps.prorail.nl/arcgis/rest/services/Water__en_Brandleidingen/FeatureServer"
    PRORAIL_FEATURE_SERVER_RD: str = "https://maps.prorail.nl/arcgis/rest/services/Riool__Drainage_en_Diesel/FeatureServer"

    BASE_DIR: Path = Path(__file__).resolve().parent.parent.parent

    @property
    def database_url(self) -> str:
        """Helper to generate the connection string."""
        return f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @computed_field  # type: ignore[prop-decorator]
    @property
    def emails_enabled(self) -> bool:
        return bool(self.SMTP_HOST and self.EMAILS_FROM_EMAIL)


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
