from pydantic import TypeAdapter
from sqlalchemy import Column, insert, select
from sqlalchemy.dialects.postgresql import VARCHAR

from src.db.connection.context_vars import db_session
from src.models import BaseDatetimeModel
from src.schemas.user import UserView


class UserModel(BaseDatetimeModel):
    """Model for users"""

    __tablename__ = "users"

    telegram_id = Column("telegram_id", VARCHAR(12), nullable=False)
    vk_access_token = Column("vk_access_token", VARCHAR(128), nullable=True)

    @classmethod
    async def create(cls, telegram_id: str, vk_access_token: str | None = None) -> UserView:
        """Create a new user db logic"""

        query = insert(UserModel).values(telegram_id=telegram_id, vk_access_token=vk_access_token).returning(UserModel)
        result = (await db_session.get().execute(query)).scalars().first()  # type: ignore
        return TypeAdapter(UserView).validate_python(result.__dict__)

    @classmethod
    async def get_by_telegram_id(cls, telegram_id: str) -> UserView | None:
        """Get user by telegram id"""

        query = select(cls).where(cls.telegram_id == telegram_id)
        result = (await db_session.get().execute(query)).scalars().first()  # type: ignore
        if result is None:
            return None
        return TypeAdapter(UserView).validate_python(result.__dict__)
