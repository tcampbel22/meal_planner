from fastapi import APIRouter, HTTPException
from sqlmodel import select
from database.database import SessionDep
from database.models import Users

router = APIRouter()


@router.get("/user/{id}")
async def get_user(id: str, session: SessionDep):
    user = session.get(Users, id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.get("/user/")
async def get_users(session: SessionDep) -> list[Users]:
    users = session.exec(select(Users)).all()
    return users


@router.post("/user/")
async def add_user(user: Users, session: SessionDep) -> Users:
    if user.username is None or user.password is None or user.email is None:
        raise HTTPException(status_code=400, detail="Bad request")
    session.add(user)
    session.commit()
    session.refresh(user)
    return user
