from pydantic import BaseSettings, Field


class AppSettings(BaseSettings):
    dask_scheduler_host: str = Field(
        env="DASK_SCHEDULER_HOST", default="scheduler:8786"
    )
    app_port: int = Field(env="APP_PORT", default=8080)
    app_host: str = Field(env="APP_HOST", default="0.0.0.0")
    database_url: str = Field(
        env="DATABASE_URL", default="postgresql+asyncpg://user:password@database/db"
    )
    shared_storage_url: str = Field(env="STORAGE", default="/storage")


def get_settings() -> AppSettings:
    return AppSettings()
