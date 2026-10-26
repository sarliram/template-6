from sqlalchemy.orm import Session
from .repository import Repository
from .schema import Create, Update

class Service:
    def __init__(self, db: Session):
        self.repo = Repository(db)

    def create(self, data: Create):
        return self.repo.create(data)
    
    def find_all(self):
        return self.repo.find_all()
    
    def find_by_id(self, id: int):
        return self.repo.find_by_id(id)
    
    def find_by_pagination(self, skip: int, take: int, sort_by: str, sort: str):
        return self.repo.find_by_pagination(skip, take, sort_by, sort)
    
    def update(self, id: int, data: Update):
        return self.repo.update(id, data)
    
    def delete(self, id: int):
        return self.repo.delete(id)

