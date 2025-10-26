from fastapi import APIRouter, Depends
from app.database.database import SessionDep
from app.api.schemas.recipe_schemas import RecipeBase, RecipeOut
from app.api.schemas.user_schemas import UserOut
from app.auth import verify_current_user
from typing import Annotated
from app.api.services.recipe_services import (
    add_new_recipe,
    get_all_recipes,
    get_all_user_recipes,
)

router = APIRouter()


@router.get("/", response_model=list[RecipeOut])
async def get_recipes(session: SessionDep) -> list[RecipeOut]:
    return await get_all_recipes(session)


@router.post("/", response_model=RecipeOut, status_code=201)
async def add_recipe(
    recipe: RecipeBase,
    current_user: Annotated[UserOut, Depends(verify_current_user)],
    session: SessionDep,
) -> RecipeOut:
    return await add_new_recipe(current_user, recipe, session)


@router.get("/me", response_model=list[RecipeBase])
async def get_user_recipes(
    session: SessionDep,
    current_user: Annotated[UserOut, Depends(verify_current_user)],
) -> list[RecipeBase]:
    return await get_all_user_recipes(current_user, session)
