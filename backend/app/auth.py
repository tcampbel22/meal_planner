from fastapi.security.oauth2 import OAuth2PasswordBearer
from app.database.database import SessionDep
from app.api.services.utils import get_user_by_email
from app.utils.exceptions import InvalidCredentialsException
from pydantic import BaseModel
from passlib.context import CryptContext
from typing import Annotated
from fastapi import Depends
from app.api.schemas.user_schemas import UserOut
import jwt
from jwt.exceptions import ExpiredSignatureError
import os
from datetime import datetime, timezone, timedelta

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/token")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET = os.getenv("JWT_SECRET")
ALGORITHM = os.getenv("ALGORITHM")


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


def hash_password(password):
    return pwd_context.hash(password)


def verify_password(password, hash_password):
    return pwd_context.verify(password, hash_password)


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET, algorithm=ALGORITHM)
    return encoded_jwt


async def verify_current_user(
    session: SessionDep, token: Annotated[str, Depends(oauth2_scheme)]
) -> UserOut:
    try:
        payload = jwt.decode(token, SECRET, algorithms=ALGORITHM)
        username = payload.get("sub")
        if username is None:
            raise InvalidCredentialsException
        token_data = TokenData(username=username)
        user = await get_user_by_email(
            email=token_data.username, session=session
        )
        if user is None:
            raise InvalidCredentialsException
        return user
    except InvalidCredentialsException:
        raise
    except ExpiredSignatureError:
        raise InvalidCredentialsException("Token is expired")
    except Exception as e:
        raise InvalidCredentialsException(f"Failed to verify user: {e}")
