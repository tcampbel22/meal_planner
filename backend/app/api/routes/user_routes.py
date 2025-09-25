from fastapi import APIRouter, Path, HTTPException, Depends
from app.database.database import SessionDep
from app.api.schemas.user_schemas import UserOut, AuthUser
from app.auth import oauth2_scheme
from typing import Annotated
import uuid
from app.api.services.user_services import (
    get_user_by_id,
    get_all_users,
    delete_user_by_id,
    add_new_user,
)

router = APIRouter()


@router.get("/{id}", response_model=UserOut)
async def get_user(
    session: SessionDep,
    token: Annotated[str, Depends(oauth2_scheme)],
    id: uuid.UUID = Path(
        title="User ID", description="The id to identify the fetched user"
    ),
) -> UserOut:
    return await get_user_by_id(id, session)


@router.get("/", response_model=list[UserOut])
async def get_users(session: SessionDep) -> list[UserOut]:
    return await get_all_users(session)


@router.post("/", status_code=201)
async def add_user(user: AuthUser, session: SessionDep) -> UserOut:
    if user.username is None or user.password is None or user.email is None:
        raise HTTPException(status_code=422, detail="Mandatory values missing")
    return await add_new_user(user, session)


@router.delete("/{id}", status_code=204, response_model=None)
async def delete_user(
    id: uuid.UUID,
    session: SessionDep,
    token: Annotated[str, Depends(oauth2_scheme)],
) -> None:
    await delete_user_by_id(id, session)
