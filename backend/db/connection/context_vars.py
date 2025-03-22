from contextvars import ContextVar

from punq import Container  # type: ignore
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession
from sqlalchemy.orm import sessionmaker


db_session: ContextVar[AsyncSession | None] = ContextVar("db_session", default=None)
container: ContextVar[Container | None] = ContextVar("container", default=None)
session_maker: ContextVar[sessionmaker | None] = ContextVar("session_maker", default=None)
engine: ContextVar[AsyncEngine | None] = ContextVar("engine", default=None)


contextvars = [db_session, container, session_maker, engine]
