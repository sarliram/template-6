from sqlalchemy import Column, Integer, String, Boolean
from database import Base

class Table(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), index=True)
    description = Column(String(100), nullable=True)