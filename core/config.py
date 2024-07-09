import secrets

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # SECRET_KEY: str = secrets.token_urlsafe(32)
    SECRET_KEY: str = "57d17c2261e04986ed3512fc37acc8c857b15584723e32fc15d45addec066e66"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    BACKEND_CORS_ORIGINS: list[str] = ["http://localhost:5173", "http://localhost:5174"]

    PROJECT_NAME: str = "Rapid Kiosk System"

    # DB_SERVER: str
    # DB_USER: str
    # DB_PASSWORD: str


settings = Settings()
