from app.database.models import Users
from app.database.database import SessionDep
from app.api.schemas.user_schemas import NewUser
from sqlmodel import select
import uuid
import bcrypt


async def get_user_by_id(id: uuid.UUID, session: SessionDep) -> Users:
    return session.get(Users, id)


async def get_all_users(session: SessionDep) -> list[Users]:
    return session.exec(select(Users)).all()


async def add_new_user(user: NewUser, session: SessionDep) -> Users:
    password = user.password
    salt = bcrypt.gensalt()
    hashed_pw = bcrypt.hashpw(password.encode("utf-8"), salt)
    db_user = Users(
        username=user.username, password=hashed_pw, email=user.email
    )
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
