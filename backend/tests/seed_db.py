from app.database.models import Users


def seed_users(session):
    users = [
        Users(username="bob", email="bob@hello.fi", password="12345"),
        Users(
            username="alice", email="alice@example.com", password="password1"
        ),
        Users(
            username="charlie",
            email="charlie@example.com",
            password="password2",
        ),
        Users(username="dave", email="dave@example.com", password="password3"),
        Users(username="eve", email="eve@example.com", password="password4"),
        Users(
            username="frank", email="frank@example.com", password="password5"
        ),
        Users(
            username="grace", email="grace@example.com", password="password6"
        ),
        Users(
            username="heidi", email="heidi@example.com", password="password7"
        ),
        Users(username="ivan", email="ivan@example.com", password="password8"),
        Users(username="judy", email="judy@example.com", password="password9"),
        Users(
            username="mallory",
            email="mallory@example.com",
            password="password10",
        ),
        Users(
            username="oscar", email="oscar@example.com", password="password11"
        ),
    ]

    for user in users:
        session.add(user)
    session.commit()
    return users
