from pydantic import BaseSettings
from pathlib import Path

class Settings(BaseSettings):
    STORAGE_PATH: str = "./storage"
    DATABASE_URL: str = "sqlite:///./data/storage.db"
    BACKEND_HOST: str = "0.0.0.0"
    BACKEND_PORT: int = 8000
    MAX_UPLOAD_SIZE: int = 1 * 1024 * 1024 * 1024  # 1 GiB

    class Config:
        env_file = "../.env"

settings = Settings()
# Ensure storage dir exists
Path(settings.STORAGE_PATH).mkdir(parents=True, exist_ok=True)
