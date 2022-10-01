from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse

from app import messages
from app.auth.models import RefreshToken
from app.auth.schemas import AuthorizationSchema, TokensSchema
from app.auth.utils import (
    AuthenticationHandler,
    PasswordHandler,
    get_auth_handler,
)
from app.base.uow import SQLAUnitOfWork
from app.users.models import User

router = APIRouter(prefix="/auth")


@router.post("/access-token/", response_model=TokensSchema)
async def generate_access_token(
    data: AuthorizationSchema,
    auth: AuthenticationHandler = Depends(get_auth_handler),
):
    uow = SQLAUnitOfWork(refresh=RefreshToken)
    user = await auth.authorize(**data.dict())
    access_token, _ = await auth.generate_token(data={"user": user.email})
    refresh_token, exp_at = await auth.generate_token(
        token_type="refresh", data={"user": user.id}
    )
    _, key, _ = refresh_token.split(".")
    async with uow:
        refresh = await uow.refresh.get_or_none(  # type: ignore
            RefreshToken.user_id == user.id
        )
        if refresh is not None:
            await uow.refresh.delete(refresh.id)  # type: ignore
        await uow.refresh.create(key=key, user_id=user.id, valid_until=exp_at)  # type: ignore
        await uow.commit()
    return TokensSchema(access_token=access_token, refresh_token=refresh_token)


@router.post("/register/")
async def register_user(data: AuthorizationSchema):
    uow = SQLAUnitOfWork(user=User)
    async with uow:
        user = await uow.user.get_or_none(User.email == data.email)  # type: ignore

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={"message": messages.NO_RECORDS_FOUND},
        )
    elif user.password is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={"message": messages.ALREADY_REGISTERED},
        )
    password_hash = PasswordHandler.get_hash(data.password)
    async with uow:
        await uow.user.update(user.id, password=password_hash)  # type: ignore
        await uow.commit()
    return JSONResponse(
        status_code=200, content={"message": messages.SUCCESSFULLY_REGISTERED}
    )


@router.post(
    "/refresh-token/",
    response_model=TokensSchema,
    response_model_include={"access_token"},
)
async def refresh_token(
    data: TokensSchema, auth: AuthenticationHandler = Depends(get_auth_handler)
):
    access_token, _ = await auth.refresh_token(**data.dict())
    return TokensSchema(access_token=access_token, refresh_token="")
