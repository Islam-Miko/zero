from pydantic import BaseModel
from typing import Optional


class UserSchema(BaseModel):
    id: Optional[int]
    email: str
    first_name: str
    last_name: str
    is_active: bool = True

    class Config:
        orm_mode = True