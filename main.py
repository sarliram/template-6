import os
from contextlib import asynccontextmanager
from pathlib import Path

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from feature.todo.routes import router as todo_router
from database import Base, engine
from mcp_server import mcp

load_dotenv(Path(__file__).parent / ".env")

mcp_app = mcp.streamable_http_app()

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with mcp.session_manager.run():
        yield

app = FastAPI(lifespan=lifespan)

Base.metadata.create_all(bind=engine)

app.include_router(todo_router)
app.router.routes.extend(mcp_app.routes)

@app.get("/")
def default():
    return {"detail": "Welcome to our api."}

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=int(os.getenv("PORT", "8000")),
        reload=True,
    )
