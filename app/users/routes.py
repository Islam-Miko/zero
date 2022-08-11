from app.base.repositories import SqlAlchemyRepository
from app.settings import get_db_session
from app.users.models import User
from app.users.schemas import UserSchema
from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter(prefix="/users")


@router.get("/users/")
async def get_users():
    session = get_db_session()
    db = SqlAlchemyRepository(session=session(), model=User)
    all_users = await db.all()
    return JSONResponse(
        status_code=200,
        content={
            "data": list(map(lambda x: x.dict(), map(UserSchema.from_orm, all_users)))
        }
    )


@router.post("/users/")
async def create_user(data: UserSchema):
    session = get_db_session()()
    db = SqlAlchemyRepository(session=session, model=User)
    created = await db.create(**data.dict())
    await session.commit()
    return JSONResponse(
        status_code=201,
        content={
            "data": UserSchema.from_orm(created).dict()
        }
    )
