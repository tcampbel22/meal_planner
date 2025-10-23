from fastapi import APIRouter, Depends
from app.database.database import SessionDep
from app.auth import verify_current_user
from typing import Annotated
from app.api.schemas.user_schemas import UserOut
from app.api.services.mealplan_services import generate_mealplan


router = APIRouter()


@router.get("/", response_model=list)
async def get_mealplan(
    session: SessionDep,
    current_user: Annotated[UserOut, Depends(verify_current_user)],
) -> list:
    return await generate_mealplan(session, current_user)
