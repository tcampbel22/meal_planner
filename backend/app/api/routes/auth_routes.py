from fastapi import APIRouter, HTTPException, Depends
from app.database.database import SessionDep
from app.api.schemas.user_schemas import AuthUser, UserOut
from app.api.services.auth_services import (
    authenticate_user,
    logout_and_blacklist_token,
)
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from typing import Annotated
from app.auth import Token, verify_current_user, oauth2_scheme
from os import getenv
from app.redis_client import get_redis
from redis import asyncio as aioredis


router = APIRouter()

TOKEN_EXP = int(getenv("TOKEN_EXPIRY", 10))


@router.post("/token")
async def login_user(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: SessionDep,
) -> Token:
    if not form_data.username or not form_data.password:
        raise HTTPException(
            status_code=422, detail="Email or password field is empty"
        )
    try:
        user = AuthUser(email=form_data.username, password=form_data.password)
    except Exception as e:
        raise HTTPException(
            status_code=422,
            detail=f"Email or password incorrectly formatted: {e}",
        )
    auth_result = await authenticate_user(user, session)
    return {"access_token": auth_result.access_token, "token_type": "bearer"}


@router.post("/logout")
async def logout_user(
    session: SessionDep,
    current_user: Annotated[UserOut, Depends(verify_current_user)],
    token: Annotated[str, Depends(oauth2_scheme)],
    redis: Annotated[aioredis.Redis, Depends(get_redis)],
) -> None:
    await logout_and_blacklist_token(token, redis)
    return {"message": f"User {current_user.username} logged out"}
