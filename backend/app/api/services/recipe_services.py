from app.database.models import Recipes
from app.database.database import SessionDep
from app.api.schemas.recipe_schemas import RecipeOut, RecipeBase
from app.api.schemas.user_schemas import UserOut
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from app.utils.exceptions import (
    DatabaseOperationException,
    DuplicateException,
    UserNotFoundException,
)
from app.database.models import Users


async def get_all_recipes(session: SessionDep) -> list[RecipeOut]:
    try:
        statement = select(
            Recipes.id,
            Recipes.user_id,
            Recipes.name,
            Recipes.url,
            Recipes.cuisine,
            Recipes.default_portion,
            Recipes.created_date,
        )
        result = session.exec(statement).all()

        recipes_data = []
        for row in result:
            recipe_dict = {
                "id": row[0],
                "user_id": row[1],
                "name": row[2],
                "url": row[3],
                "cuisine": row[4],
                "default_portion": row[5],
                "created_date": row[6],
            }
            recipes_data.append(RecipeOut(**recipe_dict))

        return recipes_data

    except Exception as e:
        raise DatabaseOperationException(f"Failed to fetch all recipes: {e}")


async def add_new_recipe(
    user: UserOut, recipe: RecipeBase, session: SessionDep
) -> RecipeOut:
    try:
        new_recipe = Recipes(
            name=recipe.name,
            url=str(recipe.url),
            user_id=user.id,
            cuisine=recipe.cuisine,
            default_portion=recipe.default_portion,
        )
        session.add(new_recipe)
        session.commit()
        session.refresh(new_recipe)

        return new_recipe

    except IntegrityError:
        session.rollback()
        raise DuplicateException("Recipe has already been added for this user")
    except Exception as e:
        session.rollback()
        raise DatabaseOperationException(
            f"Failed to add recipe {recipe.name}: {e}"
        )


async def get_all_user_recipes(
    user: UserOut, session: SessionDep
) -> list[RecipeBase]:
    try:
        user = session.get(Users, user.id)
        if not user:
            raise UserNotFoundException(f"User with {user.id} not found")
        return user.recipes
    except Exception as e:
        session.rollback()
        raise DatabaseOperationException(
            f"Failed to get user {user.username}: {e}"
        )
