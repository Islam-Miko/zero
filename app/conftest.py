import asyncio
import logging
import os

import alembic
import pytest
import pytest_asyncio
from alembic.config import Config
from sqlalchemy import text
from app.settings import Settings, get_db_session
from sqlalchemy.ext.asyncio import create_async_engine

logger = logging.getLogger(__name__)

@pytest.fixture(scope="session")
def event_loop():
    """
    Create event loop instance for testing
    """
    loop = asyncio.get_event_loop_policy().get_event_loop()
    yield loop
    loop.close()


@pytest.fixture(autouse=True)
def apply_migrations(start_db):
    os.environ["TESTING"] = "True"
    config = Config("alembic.ini")
    alembic.command.upgrade(config, "head")
    yield


@pytest_asyncio.fixture
async def session():
    session = get_db_session()()
    yield session
    await session.close()


@pytest_asyncio.fixture(scope="session",autouse=True)
async def start_db():
    settings = Settings()
    default_engine = create_async_engine(settings.database_url, isolation_level="AUTOCOMMIT")
    async with default_engine.connect() as conn:
        try:
            logging.info("zero_db_test")
            await conn.execute(
                text("DROP DATABASE IF EXISTS zero_db_test;")
            )
            await conn.execute(
                text("CREATE DATABASE zero_db_test;")
            )
        except Exception as e:
            logger.warning(e)
