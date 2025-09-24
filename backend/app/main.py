from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import user_routes, auth_routes
from app.database.database import create_db_and_tables, shutdown
from contextlib import asynccontextmanager
from app.utils.exceptions import (
    UserNotFoundException,
    DuplicateException,
    DatabaseOperationException,
    ValidationException,
    InvalidCredentialsException,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield
    shutdown()


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],
)

app.include_router(user_routes.router, prefix="/api")
app.include_router(auth_routes.router, prefix="/api")


@app.exception_handler(UserNotFoundException)
async def user_not_found_handler(request: Request, exc: UserNotFoundException):
    return JSONResponse(status_code=404, content={"detail": str(exc)})


@app.exception_handler(DuplicateException)
async def duplicate_handler(request: Request, exc: DuplicateException):
    return JSONResponse(status_code=409, content={"detail": str(exc)})


@app.exception_handler(DatabaseOperationException)
async def db_error_handler(request: Request, exc: DatabaseOperationException):
    return JSONResponse(status_code=500, content={"detail": str(exc)})


@app.exception_handler(InvalidCredentialsException)
async def invalid_credentials_handler(
    request: Request, exc: InvalidCredentialsException
):
    return JSONResponse(status_code=401, content={"detail": str(exc)})


@app.exception_handler(ValidationException)
async def validation_handler(request: Request, exc: ValidationException):
    return JSONResponse(status_code=400, content={"detail": str(exc)})


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
