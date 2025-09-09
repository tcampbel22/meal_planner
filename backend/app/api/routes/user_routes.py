from fastapi import APIRouter, HTTPException, Path
from sqlalchemy.exc import IntegrityError
from database.database import SessionDep
from api.schemas.user_schemas import NewUser, UserRead
import uuid
from api.services.user_services import (
    get_user_by_id,
    get_all_users,
    add_new_user,
    delete_user_by_id,
)

router = APIRouter()


@router.get("/user/{id}")
async def get_user(
    session: SessionDep,
    id: uuid.UUID = Path(description="The id to identify the fetched user"),
) -> UserRead:
    user = await get_user_by_id(id, session)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.get("/user/")
async def get_users(session: SessionDep) -> list[UserRead]:
    return await get_all_users(session)


@router.post("/user/", status_code=201)
async def add_user(user: NewUser, session: SessionDep) -> UserRead:
    if user.username is None or user.password is None or user.email is None:
        raise HTTPException(status_code=400, detail="Mandatory values missing")
    try:
        return await add_new_user(user, session)
    except IntegrityError:
        raise HTTPException(status_code=409, detail="Username already exists")


@router.delete("/user/{id}", status_code=204)
async def delete_user(id: uuid.UUID, session: SessionDep) -> None:
    user = await delete_user_by_id(id, session)
    if user == 404:
        raise HTTPException(status_code=404, detail="User not found")
