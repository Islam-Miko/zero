from httpx import AsyncClient

from app.base.repositories import SqlAlchemyRepository

from ..models import User


async def test_repository_user_create(client: AsyncClient, session):
    data = {
        "email": "test@gmail.com",
        "first_name": "test1",
        "last_name": "test2",
    }
    response = await client.post("/users/", json=data)
    assert response.status_code == 201

    repo = SqlAlchemyRepository(session, User)

    exists = await repo.exists(
        User.email == data["email"],
        User.first_name == data["first_name"],
        User.last_name == data["last_name"],
    )
    assert exists
