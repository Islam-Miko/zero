from pydantic import BaseModel


class AuthorizationSchema(BaseModel):
    email: str
    password: str


class TokensSchema(BaseModel):
    access_token: str
    refresh_token: str
