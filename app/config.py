from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_URL: str
    REDIS_URL: str
    EE_PROJECT: str
    EE_KEY_FILE: str = "ee_key.json"  # This has a default, so it won't crash

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
