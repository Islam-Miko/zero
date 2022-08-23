from abc import ABC, abstractmethod

from sqlalchemy.engine.result import Result

from app.base.repositories import SqlAlchemyRepository
from app.settings import get_db_session

Session = get_db_session()


class AbstractUnitOfWork(ABC):
    @abstractmethod
    async def __aenter__(self):
        raise NotImplementedError

    @abstractmethod
    async def __aexit__(self, *args):
        raise NotImplementedError

    @abstractmethod
    async def commit(self):
        raise NotImplementedError

    @abstractmethod
    async def rollback(self):
        raise NotImplementedError


class SQLAUnitOfWork(AbstractUnitOfWork):
    def __init__(self, **kwargs) -> None:
        self.__session_factory = Session
        self.__init_kwargs = kwargs

    async def __aenter__(self):
        self.__session = self.__session_factory()
        for key, model in self.__init_kwargs.items():
            repo = SqlAlchemyRepository(self.__session, model)
            setattr(self, key, repo)

    async def __aexit__(self, *args):
        await self.__session.close()

    async def commit(self):
        await self.__session.commit()

    async def rollback(self):
        await self.__session.rollback()

    async def execute(self, query) -> Result:
        result: Result = await self.__session.execute(query)
        return result
