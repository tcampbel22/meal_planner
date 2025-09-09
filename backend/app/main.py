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

app.include_router(user_routes.router, prefix="/api")
