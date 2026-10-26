from pydantic import BaseModel

class Base(BaseModel):
    title: str
    description: str 

class Create(Base):
    pass

class Response(Base):
    id: int

class Update(Base):
    id: int