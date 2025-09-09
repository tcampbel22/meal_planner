from database.models import Users
from database.database import SessionDep
from api.schemas.user_schemas import NewUser
from sqlmodel import select
import uuid


async def get_user_by_id(id: uuid.UUID, session: SessionDep) -> Users:
    return session.get(Users, id)


async def get_all_users(session: SessionDep) -> list[Users]:
    return session.exec(select(Users)).all()


async def add_new_user(user: NewUser, session: SessionDep) -> Users:
    db_user = Users(**user.model_dump())
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


async def delete_user_by_id(id: uuid.UUID, session: SessionDep) -> int:
    user = session.get(Users, id)
    if not user:
        return 404
    session.delete(user)
    session.commit()
    return 0
