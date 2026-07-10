from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_env: str = "development"
    database_url: str = "postgresql+psycopg://assistant:assistant@localhost:5432/assistant"
    redis_url: str = "redis://localhost:6379/0"
    oauth_state_secret: str = "development-only-change-me"


settings = Settings()

