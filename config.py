import os

from pydantic_settings import BaseSettings

current_path = os.path.abspath(__file__)
project_root = os.path.dirname(current_path)


class Settings(BaseSettings):
    # Настройки логгера
    LOG_FOLDER: str = f"{project_root}/logs"

    # Настройка FastApi
    APP_NAME: str = "API для вопросов и ответов"
    DEBUG: bool = False
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    class Config:
        env_file = f"{project_root}/.env"


settings = Settings()
