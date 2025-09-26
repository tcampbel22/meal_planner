from fastapi import APIRouter, HTTPException, Depends
from app.database.database import SessionDep
from app.api.schemas.user_schemas import AuthUser
from app.api.services.auth_services import authenticate_user
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from typing import Annotated
from app.auth import Token

router = APIRouter()


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
    return await authenticate_user(user, session)
