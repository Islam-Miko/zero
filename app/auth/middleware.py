import logging
import typing
from datetime import datetime

from jose import ExpiredSignatureError, JWTError, jwt
from starlette.authentication import (
    AuthCredentials,
    AuthenticationBackend,
    AuthenticationError,
)
from starlette.requests import HTTPConnection

from app.base.uow import SQLAUnitOfWork
from app.users.models import User
from app.utils import get_settings

log = logging.getLogger(__name__)


class JWTAuthentication(AuthenticationBackend):
    settings = get_settings()

    async def authenticate(
        self, conn: HTTPConnection
    ) -> typing.Optional[typing.Tuple["AuthCredentials", "User"]]:
        credentials = conn.headers.get("Authorization")
        if credentials is None:
            return AuthCredentials(["authenticated"]), None

        scheme, token = credentials.split()
        if scheme.lower() != "bearer":
            log.warning("ERROR: scheme is incorrect")
            raise AuthenticationError("Incorrect token type!")
        try:
            payload = jwt.decode(
                token,
                self.settings.secret_key,
                algorithms=self.settings.signature_algo,
            )
            email = payload.get("user")
            if email is None:
                log.warning("ERROR: something went wrong!")
                raise AuthenticationError("Wrong token!")

            if datetime.now() > datetime.fromtimestamp(
                payload.get("expiration_date")
            ):
                raise ExpiredSignatureError("Signature expired!")
        except JWTError as e:
            log.warning(f"ERROR: {e}")
            raise AuthenticationError("Failed to decode JWT!") from e
        else:
            uow = SQLAUnitOfWork(user=User)
            async with uow:
                user: User = await uow.user.get(User.email == email)  # type: ignore
            return AuthCredentials(["authenticated"]), user
