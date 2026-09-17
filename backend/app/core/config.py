from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    MAP_TILER_KEY:str
    DATABASE_URL: str

    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    ENVIRONMENT: str

    model_config = SettingsConfigDict(
        env_file=".env", extra="ignore"
    )

settings = Settings()
