from fastapi import APIRouter, HTTPException
from app.database.database import SessionDep
from app.api.schemas.auth_schemas import LoginUser
from app.api.services.auth_services import authenticate_user

router = APIRouter()


@router.post("/login/")
async def login_user(user: LoginUser, session: SessionDep):
    if not user.email or not user.password:
        raise HTTPException(
            status_code=422, detail="Email or password field is empty"
        )
    try:
        return await authenticate_user(user, session)
    except Exception as e:
        print(f"DEBUG: {e}")
        raise HTTPException(status_code=400, detail="Invalid login credentials")
