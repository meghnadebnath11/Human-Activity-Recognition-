from functools import lru_cache
from typing import List

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = Field(default="HHAR Activity Recognition API", alias="APP_NAME")
    app_env: str = Field(default="development", alias="APP_ENV")
    app_host: str = Field(default="0.0.0.0", alias="APP_HOST")
    app_port: int = Field(default=8000, alias="APP_PORT")
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")
    model_path: str = Field(default="ml/artifacts/hhar_random_forest.joblib", alias="MODEL_PATH")
    scaler_path: str = Field(default="ml/artifacts/hhar_scaler.joblib", alias="SCALER_PATH")
    label_encoder_path: str = Field(default="ml/artifacts/hhar_label_encoder.joblib", alias="LABEL_ENCODER_PATH")
    metrics_path: str = Field(default="ml/artifacts/metrics.json", alias="METRICS_PATH")
    cors_origins_raw: str = Field(
        default="http://localhost:5173,https://your-frontend-domain.vercel.app",
        alias="CORS_ORIGINS",
    )

    @property
    def cors_origins(self) -> List[str]:
        return [origin.strip() for origin in self.cors_origins_raw.split(",") if origin.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()

