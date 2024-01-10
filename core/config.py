from pydantic_settings import BaseSettings
from pathlib import Path


class Settings(BaseSettings):
    tz: str = "UTC"
    debug: bool = False
    base_path: str = str(Path(__file__).resolve().parent.parent)
    base_url: str = "http://localhost:8000"
    telegram_token: str = ""
    db_url: str = ""

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
