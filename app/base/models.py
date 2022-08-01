from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy import (
    Column, 
    Integer,
    DateTime
)

class Base:
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    
    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    deleted_at = Column(DateTime(timezone=True), nullable=True)


Base = declarative_base(cls=Base)
