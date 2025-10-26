from app.database.database import SessionDep
from app.utils.exceptions import (
    DatabaseOperationException,
    UserNotFoundException,
)
from app.database.models import Users
from app.api.schemas.user_schemas import UserOut
from app.api.schemas.mealplan_schemas import MealPlanOut


async def generate_mealplan(
    session: SessionDep, user: UserOut
) -> list[MealPlanOut]:
    try:
        db_user = session.get(Users, user.id)
        if not db_user:
            raise UserNotFoundException(f"User with {user.id} not found")
        # THIS IS A MESS NEED TO REWORK LOGIC
        recipes = db_user.recipes
        mealplans = db_user.mealplans
        final_mealplan = []
        if not mealplans:
            if len(recipes) >= 7:
                for recipe in recipes:
                    final_mealplan.append(recipe)
        else:
            sorted_plans = sorted(
                db_user.mealplans, key=lambda mp: mp.created_date, reverse=True
            )
            history = sorted_plans[:2]
            for recipe in recipes:
                if recipe.name not in history:
                    final_mealplan.append(recipe)
        print(final_mealplan)

    except Exception as e:
        session.rollback()
        raise DatabaseOperationException(f"Failed to generate mealplan: {e}")
