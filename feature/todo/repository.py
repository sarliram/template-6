from sqlalchemy.orm import Session
from sqlalchemy import asc, desc
from .model import Table
from .schema import Create, Update

class Repository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, data: Create):
        tb_data = Table(**data.dict())
        self.db.add(tb_data)
        self.db.commit()
        self.db.refresh(tb_data)
        return tb_data
    
    def find_all(self):
        return self.db.query(Table).all()

    def find_by_id(self, id: int):
        return self.db.query(Table).filter(Table.id == id).first()
    
    def find_by_pagination(self, skip: int, take: int, sort_by: str, sort: str):
        order_by_clause = asc(sort_by) if sort.lower() == "asc" else desc(sort_by)
        return self.db.query(Table).order_by(order_by_clause).offset(skip).limit(take).all()
    
    def update(self, id: int, data: Update):
        tb_data = self.find_by_id(id)
        if not tb_data:
            return None
        for key, value in data.dict(exclude_unset=True).items():
            setattr(tb_data, key, value)
        self.db.commit()
        self.db.refresh(tb_data)
        return tb_data
    
    def delete(self, id: int):
        tb_data = self.db.query(Table).filter(Table.id == id).first()
        if tb_data:
            self.db.delete(tb_data)
            self.db.commit()
            return tb_data
        return None
