from fastapi import APIRouter, Depends,HTTPException, Query
from sqlalchemy.orm import Session
from database import get_db
from .controller import Controller
from .schema import Create,Response, Update

router = APIRouter(
    prefix="/todo",
)

@router.post("/", response_model=Response)
def create(data: Create, db: Session = Depends(get_db)):
    controller = Controller(db)
    return controller.create(data)

@router.get("/all", response_model=list[Response])
def find_all(db: Session = Depends(get_db)):
    controller = Controller(db)
    return controller.find_all()

@router.get("/{skip}/{take}", response_model=list[Response])
def get_paginated_todos(
    skip: int,
    take: int,
    sort_by: str = Query("id", description="Field to sort by"),
    sort: str = Query("asc", description="Sorting order (asc or desc)"),
    db: Session = Depends(get_db),
):
    controller = Controller(db)
    return controller.find_by_pagination(skip, take, sort_by, sort)

@router.get("/{id}", response_model=Response)
def find_by_id(id: int,db:Session = Depends(get_db)):
    controller = Controller(db)
    data =  controller.find_by_id(id)
    if not data:
        raise HTTPException(status_code=404, detail="Not Found")
    return data
    
@router.put("/{id}", response_model=Response)
def update(id: int, data: Update, db: Session = Depends(get_db)):
    controller = Controller(db)
    data = controller.update(id, data)
    if not data:
        raise HTTPException(status_code=404, detail="Not Found")
    return data

@router.delete("/{id}", response_model=Response)
def delete(id: int, db: Session = Depends(get_db)):
    controller = Controller(db)
    data = controller.delete(id)
    if not data:
        raise HTTPException(status_code=404, detail="Not Found.")
    return data