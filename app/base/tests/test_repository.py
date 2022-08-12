import pytest
from sqlalchemy.orm import Session

from app.base.repositories import SqlAlchemyRepository
from app.users.models import User

pytestmark = pytest.mark.asyncio


async def test_repository_create(session: Session):
    repo = SqlAlchemyRepository(session, User)
    data = {
        "first_name": "test_user",
        "last_name": "userofich",
        "email": "testing@gmail.com",
    }
    created = await repo.create(**data)
    await session.commit()
    raw = await session.execute(
        "SELECT id, first_name, last_name, email, is_active from users"
    )
    raw = list(raw)
    assert raw is not None
    assert raw[0][0] == created.id


async def test_repository_all(session: Session):
    repo = SqlAlchemyRepository(session, User)
    count = await repo.all()
    assert len(count) == 1
    data = [
        {
            "first_name": "test_user",
            "last_name": "userofich",
            "email": "testing@gmail.com",
        },
        {
            "first_name": "test_user2",
            "last_name": "userofich2",
            "email": "testing2@gmail.com",
        },
    ]
    for item in data:
        await repo.create(**item)
    await session.commit()
    count = await repo.all()
    assert len(count) == 3


async def test_repositry_delete(session: Session):
    repo = SqlAlchemyRepository(session, User)
    count = await repo.all()
    assert len(count) > 0
    await repo.delete(count[0].id)
    after_delete = await repo.all()
    assert len(count) != len(after_delete)
