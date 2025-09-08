from fastapi import FastAPI
from api.routes import user_routes
from database.database import create_db_and_tables, shutdown
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield
    shutdown()


app = FastAPI(lifespan=lifespan)

app.include_router(user_routes.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/items/{id}")
async def read_item(id: int):
    return {"item_id": id}
