from contextvars import Token

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from backend.db.connection.context_vars import container, db_session


class Transaction:
    """
    Context manager for handling database transactions.

    This class manages the lifecycle of an asynchronous SQLAlchemy session, including:
    - Setting up the session when entering the context.
    - Committing or rolling back the transaction based on whether an exception occurred.
    - Cleaning up the session after use.

    Example usage:
    ```
    async with Transaction():
        # Perform database operations here
    ```
    """

    session: AsyncSession
    token: Token

    async def __aenter__(self):
        """
        Enter the asynchronous context and set up a new database session.

        This method:
        - Creates a new session using the resolved sessionmaker.
        - Sets the session in the `db_session` context variable.

        :return: None
        """
        session_maker = container.get().resolve(sessionmaker)
        self.session: AsyncSession = session_maker()  # type: ignore
        self.token = db_session.set(self.session)

    async def __aexit__(self, exception_type, exception, traceback):
        """
        Exit the asynchronous context, handling commit or rollback.

        This method:
        - Rolls back the transaction if an exception occurred.
        - Commits the transaction otherwise.
        - Closes the session and resets the `db_session` context variable.

        :param exception_type: Type of the exception, if any.
        :param exception: The exception instance, if any.
        :param traceback: Traceback object, if any.
        :return: None
        """
        if exception:
            await self.session.rollback()
        else:
            await self.session.commit()
        await self.session.close()
        db_session.reset(self.token)
