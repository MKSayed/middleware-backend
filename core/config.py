import secrets

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    BACKEND_CORS_ORIGINS: list[str] = ["http://localhost:5173",]

    PROJECT_NAME: str = "Rapid Kiosk Systems"

    # DB_SERVER: str
    # DB_USER: str
    # DB_PASSWORD: str


settings = Settings()
