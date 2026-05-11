from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    # Database
    database_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/quickt_db"

    # Security
    secret_key: str = "dev-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60
    refresh_token_expire_days: int = 30

    # Application
    app_env: str = "development"
    cors_origins: list[str] = ["http://localhost:3001", "http://localhost:3002"]

    # Storage (local or s3)
    storage_backend: str = "local"
    upload_dir: str = "uploads"
    upload_max_size_mb: int = 5
    upload_base_url: str = ""

    # S3 settings
    s3_bucket: str = ""
    s3_region: str = ""
    s3_access_key: str = ""
    s3_secret_key: str = ""
    s3_endpoint_url: str = ""

    # AWS / Email (SES)
    aws_access_key_id: str = ""
    aws_secret_access_key: str = ""
    aws_region: str = "us-east-1"
    aws_ses_sender_email: str = "noreply@quickt.tg"
    aws_ses_sender_name: str = "QuickT"
    aws_ses_configuration_set: str | None = None
    email_enabled: bool = False

    # Sentry / error tracking
    sentry_dsn: str = ""

    # Frontend URL
    frontend_url: str = "http://localhost:3001"

    # Mobile Money
    momo_provider: str = "sandbox"  # sandbox, paygate, cinetpay
    momo_api_key: str = ""
    momo_api_secret: str = ""
    momo_site_id: str = ""

    @property
    def is_production(self) -> bool:
        return self.app_env == "production"

    @property
    def is_testing(self) -> bool:
        return self.app_env == "testing"


@lru_cache
def get_settings() -> Settings:
    return Settings()
