from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime

from . import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    full_name = Column(String, nullable=False)
    join_date = Column(DateTime, default=datetime.utcnow)
    points = Column(Integer, default=0)

