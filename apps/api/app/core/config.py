from pydantic import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    APP_ENV: str = "development"
    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = 8000
    # Reminder offsets in minutes; code expects a list of ints. Change as needed.
    REMINDER_OFFSETS_MINUTES: list = [10]

    class Config:
        env_file = "../../.env"
        env_file_encoding = "utf-8"


settings = Settings()
