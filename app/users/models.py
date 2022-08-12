from sqlalchemy import Boolean, Column, String
from sqlalchemy_utils import EmailType

from app.base.models import Base


class User(Base):
    __tablename__ = "users"

    email = Column(EmailType, unique=True)
    password = Column(String)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    image = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
