from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./app.db"
    ALLOW_ORIGINS: list[str] = ["*"]

settings = Settings()
