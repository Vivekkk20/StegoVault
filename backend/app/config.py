"""
StegoVault Configuration & Settings
"""
from pathlib import Path
from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "StegoVault"
    APP_ENV: str = "development"
    DEBUG: bool = True
    HOST: str = "127.0.0.1"
    PORT: int = 8000
    
    # Security
    SECRET_KEY: str = "stegovault-insecure-dev-secret-key-replace-in-prod-32ch"
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
    ]
    MAX_UPLOAD_SIZE_BYTES: int = 20 * 1024 * 1024  # 20 MB
    PBKDF2_ITERATIONS: int = 600_000  # OWASP recommendation

    def model_post_init(self, __context):
        if self.APP_ENV.lower() in ("test", "testing"):
            self.PBKDF2_ITERATIONS = 1000
    
    # Storage
    BASE_DIR: Path = Path(__file__).resolve().parent.parent
    STORAGE_DIR: Path = Path(__file__).resolve().parent.parent / "storage"
    TEMP_DIR: Path = Path(__file__).resolve().parent.parent / "storage" / "temp"
    REPORTS_DIR: Path = Path(__file__).resolve().parent.parent / "storage" / "reports"
    
    # Logging
    LOG_LEVEL: str = "INFO"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


settings = Settings()

# Ensure directories exist
settings.TEMP_DIR.mkdir(parents=True, exist_ok=True)
settings.REPORTS_DIR.mkdir(parents=True, exist_ok=True)
