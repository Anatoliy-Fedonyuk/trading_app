from sqlalchemy import Column, Integer, String

from src.database import Base


class Messages(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True)
    messages = Column(String(length=1024), nullable=False)
