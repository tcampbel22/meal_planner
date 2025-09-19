from fastapi import APIRouter, HTTPException
from app.database.database import SessionDep
from api.schemas.auth_schemas import LoginUser
from api.services.auth_services import authenticate_user

router = APIRouter()


@router.post("/login/")
async def login_user(user: LoginUser, session: SessionDep):
    if not user.email or not user.password:
        raise HTTPException(
            status_code=422, detail="Email or password field is empty"
        )
    try:
        return await authenticate_user(user)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid login credentials")
