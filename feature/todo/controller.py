
from sqlalchemy.orm import Session
from .service import Service
from .schema import Create, Update

class Controller:
    def __init__(self, db: Session):
        self.service = Service(db)

    def create(self, data:Create ):
        return self.service.create(data)
    
    def find_all(self):
        return self.service.find_all()

    def find_by_id(self, id: int):
        return self.service.find_by_id(id)
    
    def find_by_pagination(self, skip: int, take: int, sort_by: str, sort: str):
        return self.service.find_by_pagination(skip, take, sort_by, sort)
    
    def update(self, id: int, data: Update):
        return self.service.update(id, data)
    
    def delete(self, id: int):
        return self.service.delete(id)
