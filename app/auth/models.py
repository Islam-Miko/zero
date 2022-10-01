from sqlalchemy import Column, Float, ForeignKey, Integer, String

from app.base.models import Base


class RefreshToken(Base):
    __tablename__ = "refresh_token"

    key = Column(String(255), nullable=False)
    valid_until = Column(Float, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    # user = relationship("User", lazy="subquery")
