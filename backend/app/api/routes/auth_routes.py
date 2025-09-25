from fastapi import APIRouter, HTTPException
from app.database.database import SessionDep
from app.api.schemas.user_schemas import AuthUser, UserOut
from app.api.services.auth_services import authenticate_user

router = APIRouter()


@router.post("/login/")
async def login_user(user: AuthUser, session: SessionDep) -> UserOut:
    if not user.email or not user.password:
        raise HTTPException(
            status_code=422, detail="Email or password field is empty"
        )
    return await authenticate_user(user, session)
