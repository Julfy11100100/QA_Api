import os

from pydantic_settings import BaseSettings

current_path = os.path.abspath(__file__)
project_root = os.path.dirname(current_path)


class Settings(BaseSettings):
    # Настройки логгера
    LOG_FOLDER: str = f"{project_root}/logs"
    LOG_LEVEL: str = "ERROR"

    # Настройка FastApi
    APP_NAME: str = "API для вопросов и ответов"
    DEBUG: bool = False
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # Настройки параметров вопросов и ответов
    Q_MIN_LENGTH: int = 1
    Q_MAX_LENGTH: int = 1000
    A_MIN_LENGTH: int = 1
    A_MAX_LENGTH: int = 1000

    # Настройка базы данных
    DATABASE_URL: str = "postgres://postgres:postgres@postgres:5433/app_dbb"
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    PGDATA: str = "/var/lib/postgresql/data/pgdata"

    class Config:
        env_file = f"{project_root}/.env"


settings = Settings()
