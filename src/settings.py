# pylint: disable=E0213
# disabled E0213 because Method 'assemble_postgres_db_url' should have "self" as first argument (no-self-argument)
# but if replace `cls` with `self` raise PydanticUserError
# pydantic.errors.PydanticUserError: `@field_validator` cannot be applied to instance methods

from functools import lru_cache
from typing import Any

from pydantic import SecretStr, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Settings for database connection"""

    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: SecretStr
    POSTGRES_POOL_SIZE: int = 10
    POSTGRES_POOL_TIMEOUT: int = 30
    DATABASE_URL: str | None = None

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=False, extra="ignore", env_prefix="BACKEND_")

    @field_validator("DATABASE_URL", mode="before")  # type: ignore
    def assemble_postgres_db_url(cls, v: str | None, values: Any) -> str:
        """Auto assembling postgres db url function"""
        if v and isinstance(v, str):
            return v
        return (
            f"postgresql+psycopg2://"
            f"{values.data['POSTGRES_USER']}:{values.data['POSTGRES_PASSWORD'].get_secret_value()}@"
            f"{values.data['POSTGRES_HOST']}:{values.data['POSTGRES_PORT']}/"
            f"{values.data['POSTGRES_DB']}"
        )


@lru_cache
def get_settings() -> Settings:
    """Cached settings function"""
    return Settings()  # type: ignore