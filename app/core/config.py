"""Application Configuration using Pydantic Settings."""

from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """MuniAudit-AI Core Application Settings."""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    APP_NAME: str = "MuniAudit-AI"
    APP_ENV: str = "development"
    DEBUG: bool = True
    PORT: int = 8000
    HOST: str = "0.0.0.0"
    LOG_LEVEL: str = "INFO"

    # Security
    SECRET_KEY: str = "muniaudit_default_development_secret_key_12345"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 480

    # Database
    DATABASE_URL: str = (
        "postgresql://muniaudit_admin:muniaudit_secure_password@localhost:5432/muniaudit_db"
    )

    # Storage
    STORAGE_BACKEND: str = "local"  # "local" or "s3"
    LOCAL_STORAGE_PATH: Path = Path("./data/evidence_storage")
    AWS_REGION: str = "ap-south-1"
    AWS_S3_EVIDENCE_BUCKET: str = "muniaudit-evidence-store-dev"

    # Queue (SQS)
    SQS_QUEUE_URL: str = ""
    SQS_DLQ_URL: str = ""

    # Civil & Physical Invariants
    MASS_BALANCE_TOLERANCE_KG: float = 20.0
    MAX_SILT_DENSITY_T_M3: float = 1.90
    GEODESIC_SPEED_CEILING_KMH: float = 80.0
    SSCD_SIMILARITY_THRESHOLD: float = 0.82


settings = Settings()
