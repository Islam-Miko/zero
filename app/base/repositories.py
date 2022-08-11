import abc
from datetime import datetime
from typing import Any
from sqlalchemy.orm import Session
from app.base.models import Base as Model
from sqlalchemy.future import select
from sqlalchemy.engine import ResultProxy
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import update


class ABCRepository(abc.ABC):

    @abc.abstractmethod
    async def create(self, data: dict[str, Any])-> None:
        raise NotImplementedError

    @abc.abstractmethod
    async def get(self, pk: Any)-> Any:
        raise NotImplementedError

    @abc.abstractmethod
    async def delete(self, pk: Any)-> None:
        raise NotImplementedError

    @abc.abstractmethod
    async def update(self, *args, **kwargs)-> Any:
        raise NotImplementedError


class SqlAlchemyRepository(ABCRepository):
    def __init__(self, session: Session, model: Model) -> None:
        self.__session = session
        self.model = model

    async def create(self, **data: dict[str, Any]) -> None:
        instance = self.model(**data)
        self.__session.add(instance)
        await self.__session.flush()
        return instance

    async def get(self, *args: Any, **kwargs: Any) -> Any:
        try:
            query = (
                select(self.model)
                .filter(*args, **kwargs)
            )
            result: ResultProxy = await self.__session.execute(query)
            return result.scalars().one()
        except NoResultFound:
            raise #TODO create new Exception to catch in server.py

        
    async def delete(self, pk: Any)-> None:
        try:
            query = (
                update(self.model)
                .filter(self.model.id == pk)
                .returning(self.model)
                .values(deleted_at=datetime.now())
            )
            result: ResultProxy = await self.__session.execute(query)
            return result.one_or_none()
        except NoResultFound:
            raise

    async def update(self, pk: Any, **kwargs: Any)-> None:
        try:
            query = (
                update(self.model)
                .filter(self.model.id == pk)
                .returning(self.model)
                .values(**kwargs)
            )
            result: ResultProxy = await self.__session.execute(query)
            return result.first()
        except NoResultFound:
            raise

    async def all(self, *args: Any, **kwargs: Any)-> Any:
        query = (
            select(
                self.model
            )
            .filter(self.model.deleted_at.is_(None))
        )
        if args:
            query.filter(*args)
        result: ResultProxy = await self.__session.execute(query)
        return result.scalars().all()
