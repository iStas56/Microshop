from asyncio import current_task

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
    async_sessionmaker,
    async_scoped_session,
)

from core.config import settings


class DatabaseHelper:
    """
    DatabaseHelper class provides a convenient interface for working with the database.

    Args:
        url (str): The URL of the database.
        echo (bool, optional): A flag to enable SQL query output. Defaults to False.
    """

    def __init__(self, url: str, echo: bool = False):
        """
        Initializes an instance of the DatabaseHelper class.

        Creates an asynchronous engine and session factory for interacting with the database.

        Args:
            url (str): The URL of the database.
            echo (bool, optional): A flag to enable SQL query output. Defaults to False.
        """
        # Create an asynchronous engine to interact with the database
        self.engine = create_async_engine(
            url=url,
            echo=echo,
        )
        # Create a session factory for managing database sessions
        self.session_factory = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        )

    def get_scoped_session(self):
        """
        Creates and returns a scoped session.

        This scoped session is tied to the current asyncio task,
        allowing for session management within the context of a single task.

        Returns:
            async_scoped_session: A scoped session object.
        """
        session = async_scoped_session(
            session_factory=self.session_factory,
            scopefunc=current_task,
        )
        return session

    async def session_dependency(self) -> AsyncSession:
        """
        Provides a session for dependency injection in FastAPI routes.

        This method is used to manage the lifecycle of a session,
        ensuring that it is properly closed after use.

        Yields:
            AsyncSession: An asynchronous database session.
        """
        async with self.session_factory() as session:
            yield session
            await session.close()

    async def scoped_session_dependency(self) -> AsyncSession:
        session = self.get_scoped_session()
        yield session
        await session.close()


# Create an instance of the DatabaseHelper class using parameters from the settings module.
db_helper = DatabaseHelper(
    url=settings.db_url,
    echo=settings.db_echo,
)
