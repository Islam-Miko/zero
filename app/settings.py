from typing import Callable
from pydantic import BaseSettings
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import Session, sessionmaker

class Settings(BaseSettings):
    database_url: str
    testing: bool = False

    class Config:
        env_file = ".env"

    

def get_db_session()-> Callable[..., Session]:
    settings = Settings()
    database_url = f"{settings.database_url}_test" if settings.testing else settings.database_url 
    async_engine = create_async_engine(database_url, future=True, echo=True)
    return sessionmaker(
        async_engine,
        expire_on_commit=False,
        class_=AsyncSession
    )