from app.database.models import Users
from app.database.database import SessionDep
from app.api.schemas.auth_schemas import LoginUser
from app.utils.exceptions import (
    InvalidCredentialsException,
    UserNotFoundException,
)
from sqlalchemy import select
import bcrypt


async def authenticate_user(user: LoginUser, session: SessionDep):
    query = select(Users).where(Users.email == user.email)
    data = session.exec(query).scalar_one_or_none()
    if not data:
        raise UserNotFoundException("User not found")
    validate = bcrypt.checkpw(user.password.encode("utf-8"), data.password)
    if not validate:
        raise InvalidCredentialsException("Invalid password or email")
    return data
