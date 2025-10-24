from app.database.models import Users
from app.auth import hash_password


def seed_users(session):
    created_users = []

    bob_user = Users(
        username="bob",
        email="bob@hello.fi",
        password=hash_password("12345"),
        recipes=[],
        mealplans=[],
    )
    session.add(bob_user)
    created_users.append(bob_user)

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

    session.commit()
    for user in created_users:
        session.refresh(user)

    return created_users
