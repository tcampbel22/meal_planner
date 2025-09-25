from app.database.models import Users
from app.database.database import SessionDep
from app.api.schemas.user_schemas import AuthUser, UserOut
from app.utils.exceptions import (
    InvalidCredentialsException,
    UserNotFoundException,
    DatabaseOperationException,
)
from sqlalchemy import select
import bcrypt


async def authenticate_user(user: AuthUser, session: SessionDep) -> UserOut:
    query = select(Users).where(Users.email == user.email)
    try:
        data = session.exec(query).scalar_one_or_none()
        if not data:
            raise UserNotFoundException(
                f"User with email {user.email} not found"
            )

        validate = bcrypt.checkpw(
            user.password.encode("utf-8"), data.password.encode("utf-8")
        )
        if not validate:
            raise InvalidCredentialsException("Invalid password or email")

        return UserOut(
            id=data.id,
            username=data.username,
            email=data.email,
            created_date=data.created_date,
        )
    except (UserNotFoundException, InvalidCredentialsException):
        raise
    except Exception as e:
        raise DatabaseOperationException(f"Authentication error: {e}")
