from typing import Optional

from pydantic import BaseModel


class UserSchema(BaseModel):
    id: Optional[int]
    email: str
    first_name: str
    last_name: str
    is_active: bool = True

    class Config:
        orm_mode = True
