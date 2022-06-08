from pydantic import BaseSettings
from sqlalchemy.ext.asyncio import create_async_engine

class Settings(BaseSettings):
    db_url: str


settings = Settings()
async_engine = create_async_engine(settings.db_address, future=True)