from fastapi import APIRouter, HTTPException, Path
from app.database.database import SessionDep
from app.api.schemas.user_schemas import NewUser, UserOut
import uuid
from app.api.services.user_services import (
    get_user_by_id,
    get_all_users,
    add_new_user,
    delete_user_by_id,
)

router = APIRouter()


@router.get("/user/{id}", response_model=UserOut)
async def get_user(
    session: SessionDep,
    id: uuid.UUID = Path(
        title="User ID", description="The id to identify the fetched user"
    ),
) -> UserOut:
    return await get_user_by_id(id, session)


@router.get("/user/", response_model=list[UserOut])
async def get_users(session: SessionDep) -> list[UserOut]:
    return await get_all_users(session)


@router.post("/user/", status_code=201)
async def add_user(user: NewUser, session: SessionDep) -> UserOut:
    if user.username is None or user.password is None or user.email is None:
        raise HTTPException(status_code=422, detail="Mandatory values missing")
    return await add_new_user(user, session)


@router.delete("/user/{id}", status_code=204, response_model=None)
async def delete_user(id: uuid.UUID, session: SessionDep) -> None:
    await delete_user_by_id(id, session)
