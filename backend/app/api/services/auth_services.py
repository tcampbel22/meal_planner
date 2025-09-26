from app.database.database import SessionDep
from app.api.services.utils import get_user_by_email
from app.api.schemas.user_schemas import AuthUser
from app.auth import Token, create_access_token
from app.utils.exceptions import (
    InvalidCredentialsException,
    UserNotFoundException,
    DatabaseOperationException,
)
from os import getenv
from datetime import timedelta
from app.auth import verify_password

TOKEN_EXP = int(getenv("TOKEN_EXPIRY", 10))


async def authenticate_user(user: AuthUser, session: SessionDep) -> Token:
    try:
        data = await get_user_by_email(user.email, session)
        if not data:
            raise UserNotFoundException(
                f"User with email {user.email} not found"
            )
        validate = verify_password(user.password, data.password)
        if not validate:
            raise InvalidCredentialsException("Invalid password or email")

        token_expiry = timedelta(minutes=TOKEN_EXP)
        token = create_access_token(
            data={"sub": user.email}, expires_delta=token_expiry
        )
        return Token(access_token=token, token_type="bearer")
    except (UserNotFoundException, InvalidCredentialsException):
        raise
    except Exception as e:
        raise DatabaseOperationException(f"Authentication error: {e}")
