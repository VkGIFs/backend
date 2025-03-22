import uuid

from pydantic import BaseModel


class UserView(BaseModel):
    """User View Schema"""

    id: uuid.UUID
    telegram_id: str
    vk_access_token: str


class UserCreateView(BaseModel):
    """User Create Schema"""

    telegram_id: str
    vk_access_token: str | None = None
