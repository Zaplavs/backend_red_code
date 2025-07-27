from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    ADMIN_EMAIL: str
    ADMIN_PASSWORD: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    # Новые настройки для базы данных
    DB_HOST: str = "localhost"
    DB_PORT: str = "5432"
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str

    class Config:
        env_file = ".env"

settings = Settings()