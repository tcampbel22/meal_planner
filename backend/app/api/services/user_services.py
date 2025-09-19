from app.database.models import Users
from app.database.database import SessionDep
from app.api.schemas.user_schemas import NewUser, UserOut
from app.utils.exceptions import (
    UserNotFoundException,
    DuplicateException,
    DatabaseOperationException,
)
from sqlalchemy.exc import IntegrityError
from sqlmodel import select
import uuid
import bcrypt


async def get_user_by_id(id: uuid.UUID, session: SessionDep) -> UserOut:
    user = session.get(Users, id)
    if not user:
        raise UserNotFoundException(f"User with {id} not found")
    return user


async def get_all_users(session: SessionDep) -> list[Users]:
    return session.exec(select(Users)).all()


async def add_new_user(user: NewUser, session: SessionDep) -> UserOut:
    try:
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
    except IntegrityError as e:
        session.rollback()
        err_message = str(e.orig)

        if "username_key" in err_message:
            raise DuplicateException(f"Username {user.username} already exists")
        elif "email_key" in err_message:
            raise DuplicateException(f"Email {user.email} already exists")
        else:
            raise DuplicateException("Duplicate value error")
    except Exception as e:
        session.rollback()
        raise DatabaseOperationException(
            f"Failed to create user {user.username}: str{e}"
        )


async def delete_user_by_id(id: uuid.UUID, session: SessionDep) -> None:
    try:
        user = session.get(Users, id)
        if not user:
            raise UserNotFoundException(f"User with {id} not found")
        session.delete(user)
        session.commit()
    except Exception as e:
        session.rollback()
        raise DatabaseOperationException(
            f"Failed to delete user {user.username}: str{e}"
        )
