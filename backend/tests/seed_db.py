from app.database.models import Users, Recipes
from app.auth import hash_password
from sqlalchemy import select


def seed_users(session):
    created_users = []

    for i in range(1, 12):
        db_user = Users(
            username=f"user{i}",
            email=f"user{i}@example.com",
            password=hash_password(f"password{i}"),
            recipes=[],
            mealplans=[],
        )
        session.add(db_user)
        created_users.append(db_user)

    return created_users


def seed_one_user(session):
    bob_user = Users(
        username="bob",
        email="bob@hello.fi",
        password=hash_password("12345"),
        recipes=[],
        mealplans=[],
    )
    session.add(bob_user)
    return bob_user


def seed_recipes(session):
    query = select(Users).where(Users.username == "bob")
    user = session.exec(query).scalar_one_or_none()

    if not user:
        raise Exception(
            "User 'bob' not found. Make sure user seeding runs first."
        )

    recipes_to_create = [
        Recipes(
            name="Pasta Carbonara",
            url="https://www.italy.com",
            cuisine="Italian",
            user_id=user.id,
        ),
        Recipes(
            name="Chicken Curry",
            url="https://www.india.com",
            cuisine="Indian",
            user_id=user.id,
        ),
        Recipes(
            name="Tacos",
            url="https://www.mexico.com",
            cuisine="Mexican",
            user_id=user.id,
        ),
    ]

    session.add_all(recipes_to_create)
    return recipes_to_create
