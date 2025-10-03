from app.database.models import Users
from app.database.database import SessionDep
from app.api.schemas.user_schemas import UserOut, AuthUser
from app.utils.exceptions import (
    UserNotFoundException,
    DatabaseOperationException,
    DuplicateException,
)
from sqlalchemy.exc import IntegrityError
from sqlmodel import select
from app.auth import hash_password
import uuid


async def get_user_by_id(id: uuid.UUID, session: SessionDep) -> UserOut:
    try:
        user = session.get(Users, id)
        if not user:
            raise UserNotFoundException(f"User with {id} not found")
        safeUser = user.model_dump(exclude={"password"})
        return safeUser
    except UserNotFoundException:
        raise
    except Exception as e:
        raise DatabaseOperationException(f"Failed to fetch user {id}: {e}")


async def get_all_users(session: SessionDep) -> list[UserOut]:
    try:
        users = session.exec(select(Users)).all()
        safeUsers = [user.model_dump(exclude={"password"}) for user in users]
        return safeUsers
    except Exception as e:
        raise DatabaseOperationException(f"Failed to fetch all users: {e}")


async def add_new_user(user: AuthUser, session: SessionDep) -> UserOut:
    try:
        hashed_pw = hash_password(user.password)
        db_user = Users(
            username=user.username,
            password=hashed_pw,
            email=user.email,
        )
        session.add(db_user)
        session.commit()
        session.refresh(db_user)
        safe_user = db_user.model_dump(exclude={"password"})
        return safe_user
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
            f"Failed to create user {user.username}: {e}"
        )


async def delete_user_by_id(id: uuid.UUID, session: SessionDep) -> None:
    try:
        user = session.get(Users, id)
        if not user:
            raise UserNotFoundException(f"User with {id} not found")
        session.delete(user)
        session.commit()
    except UserNotFoundException:
        raise
    except Exception as e:
        session.rollback()
        raise DatabaseOperationException(
            f"Failed to delete user {user.username}: str{e}"
        )
