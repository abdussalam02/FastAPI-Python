from email.policy import default
from sqlalchemy import Boolean, Column, Integer, String, DateTime
from sqlalchemy.sql import func
from database import Base

class Todos(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True)
    work = Column(String(100))
    complete = Column(Boolean, default=False)
    time_created = Column(DateTime(timezone=True), server_default=func.now())