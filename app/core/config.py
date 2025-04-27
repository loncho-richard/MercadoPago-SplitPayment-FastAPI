from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///database.db"
    SECRET_KEY: str = ""
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    CORS_ORIGINS: list[str] = ["*"]
    MP_PUBLIC_KEY: str = ""
    MP_ACCESS_TOKEN: str = ""
    MP_CLIENT_ID: str = ""
    MP_CLIENT_SECRET: str = ""
    DOMAIN: str = "http://127.0.0.1:8000"

    model_config = SettingsConfigDict(
        env_file = ".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )
        

settings = Settings()