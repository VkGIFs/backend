# pylint: disable=too-few-public-methods,not-callable
import uuid

from sqlalchemy import Column, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base


Base = declarative_base()


class BaseModel(Base):  # type: ignore
    """Abstract base model for all db tables"""

    __abstract__ = True

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)


class BaseDatetimeModel(BaseModel):
    """Abstract datetime model for all db tables"""

    __abstract__ = True

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    deleted_at = Column(DateTime, nullable=True)
