from datetime import datetime, timedelta
from functools import lru_cache
from typing import Any, Dict

from jose import jwt
from passlib.context import CryptContext
from starlette.authentication import AuthenticationError

from app.base.uow import SQLAUnitOfWork
from app.users.models import User
from app.utils import get_settings


class PasswordHandler:
    context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    @classmethod
    def verify_password(cls, plain_pass: str, hash_pass: str):
        return cls.context.verify(plain_pass, hash_pass)

    @classmethod
    def get_hash(cls, password: str):
        return cls.context.hash(password)


class AuthenticationHandler:
    handler = PasswordHandler
    settings = get_settings()

    async def authorize(self, email: str, password: str):
        uow = SQLAUnitOfWork(user=User)
        async with uow:
            user = await uow.user.get_or_none(User.email == email)  # type: ignore

        if user is None:
            raise AuthenticationError("Invalid credentials.")

        if not self.handler.verify_password(password, user.password):
            raise AuthenticationError("Invalid credentials.")
        return user

    async def generate_token(
        self, token_type: str = "access", data: Dict[str, Any] = dict()
    ):
        token_lifetime = {
            "access": self.settings.access_token_lifetime,
            "refresh": self.settings.refresh_token_lifetime,
        }
        expires_delta = timedelta(minutes=token_lifetime.get(token_type))
        expires_at = datetime.timestamp(datetime.now() + +expires_delta)
        data.update({"expiration_date": expires_at})
        encoded = jwt.encode(
            data, self.settings.secret_key, self.settings.signature_algo
        )
        return encoded

    async def refresh_token(self, refresh_token: str) -> str:
        # payload = jwt.decode(
        #     refresh_token,
        #     self.settings.signature_algo,
        #     options={"verify_exp": False},
        # )
        pass
        # TODO implement refresh token rotation


@lru_cache
def get_auth_handler():
    return AuthenticationHandler()
