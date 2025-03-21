from uuid import UUID

from pydantic import BaseModel, Field

from src.settings import get_settings


class AccessTokenView(BaseModel):
    """JWT access token model"""

    jti: str | None
    iss: str = Field(default_factory=lambda: get_settings().APP_NAME)
    sub: str | UUID
    telegram_id: str


class RefreshTokenView(BaseModel):
    """JWT refresh token model"""

    iss: str = Field(default_factory=lambda: get_settings().APP_NAME)
    sub: str | UUID
    exp: float


class TokensView(BaseModel):
    """JWT tokens model"""

    access_token: str
    refresh_token: str
    exp: float
