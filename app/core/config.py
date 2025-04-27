from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Literal

class Settings(BaseSettings):
    ENVIRONMENT: Literal["development", "production"] = "development"
    
    DATABASE_URL: str = "sqlite:///database.db"
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    CORS_ORIGINS: list[str] = ["*"]
    DOMAIN: str = "localhost"
    
    # Mercado Pago
    MP_CLIENT_ID: str
    MP_CLIENT_SECRET: str
    MP_MARKETPLACE_FEE: float = 0.05  # 5% fee

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()