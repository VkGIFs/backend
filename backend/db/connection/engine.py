from punq import Container  # type: ignore
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from backend.db.connection.context_vars import container, engine, session_maker
from backend.settings import Settings


def setup_db_connection(settings: Settings):
    """
    Configures the PostgreSQL SQLAlchemy.

    This function sets up:
    - An asynchronous SQLAlchemy engine.
    - A session maker for managing database sessions.
    - A dependency injection container to manage session maker instances.

    Args:
        settings (Settings): The settings containing the `DATABASE_URL`
                                     and other PostgreSQL configuration details.

    Example:
        from postgres_sqlalchemy_sdk.settings import PostgresSettings

        settings = PostgresSettings(DATABASE_URL="postgresql+asyncpg://user:password@localhost/db")
        setup_postgres_sqlalchemy_sdk(settings)
    """

    if settings.DATABASE_URL is None:
        raise RuntimeError("DATABASE_URL must be set")

    local_engine = create_async_engine(
        settings.DATABASE_URL,
        echo=True,
        pool_size=settings.POSTGRES_POOL_SIZE,
        pool_timeout=settings.POSTGRES_POOL_TIMEOUT,
        future=True,
    )
    local_session_maker = sessionmaker(bind=local_engine, class_=AsyncSession, expire_on_commit=False)  # type: ignore

    class SessionMaker:  # pylint: disable=too-few-public-methods
        """
        A class to encapsulate the session maker logic.

        The `__new__` method ensures that a new session maker is created with the
        provided engine and AsyncSession settings when instantiated.
        """

        def __new__(cls):
            return sessionmaker(local_engine, class_=AsyncSession, expire_on_commit=False)

    # Set up the dependency injection container
    local_container = Container()
    local_container.register(sessionmaker, SessionMaker)

    # Store the components in context variables
    engine.set(local_engine)
    session_maker.set(local_session_maker)
    container.set(local_container)
