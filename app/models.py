from sqlalchemy import Column, Integer, String
from app.database import Base


class UserInfo(Base):
    __tablename__ = "user_info"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, nullable=False)
    name = Column(String, nullable=False)
    locale = Column(String, nullable=True, server_default="en")
