from typing import Literal, Optional

from database import SessionLocal
from .controller import Controller
from .schema import Create, Response, Update


def serialize(item) -> dict:
    return Response.model_validate(item, from_attributes=True).model_dump()


def create_todo(title: str, description: str) -> dict:
    """Create a new todo item."""
    with SessionLocal() as db:
        return serialize(Controller(db).create(Create(title=title, description=description)))


def list_todos() -> list[dict]:
    """List all todo items."""
    with SessionLocal() as db:
        return [serialize(item) for item in Controller(db).find_all()]


def list_todos_paginated(
    skip: int = 0,
    take: int = 10,
    sort_by: Literal["id", "title", "description"] = "id",
    sort: Literal["asc", "desc"] = "asc",
) -> list[dict]:
    """List todo items with pagination and sorting."""
    with SessionLocal() as db:
        return [serialize(item) for item in Controller(db).find_by_pagination(skip, take, sort_by, sort)]


def get_todo(id: int) -> dict:
    """Get a single todo item by its id."""
    with SessionLocal() as db:
        item = Controller(db).find_by_id(id)
        if not item:
            raise ValueError(f"Todo {id} not found")
        return serialize(item)


def update_todo(id: int, title: Optional[str] = None, description: Optional[str] = None) -> dict:
    """Update a todo item. Fields that are not provided keep their current value."""
    with SessionLocal() as db:
        controller = Controller(db)
        existing = controller.find_by_id(id)
        if not existing:
            raise ValueError(f"Todo {id} not found")
        data = Update(
            id=id,
            title=title if title is not None else existing.title,
            description=description if description is not None else existing.description,
        )
        return serialize(controller.update(id, data))


def delete_todo(id: int) -> dict:
    """Delete a todo item by its id."""
    with SessionLocal() as db:
        item = Controller(db).delete(id)
        if not item:
            raise ValueError(f"Todo {id} not found")
        return serialize(item)


tools = [create_todo, list_todos, list_todos_paginated, get_todo, update_todo, delete_todo]
