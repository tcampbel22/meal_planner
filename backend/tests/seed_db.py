from app.database.models import Users
from app.auth import hash_password

users = [
    {"username": "bob", "email": "bob@hello.fi", "password": "12345"},
    {
        "username": "alice",
        "email": "alice@example.com",
        "password": "password1",
    },
    {
        "username": "charlie",
        "email": "charlie@example.com",
        "password": "password2",
    },
    {"username": "dave", "email": "dave@example.com", "password": "password3"},
    {"username": "eve", "email": "eve@example.com", "password": "password4"},
    {
        "username": "frank",
        "email": "frank@example.com",
        "password": "password5",
    },
    {
        "username": "grace",
        "email": "grace@example.com",
        "password": "password6",
    },
    {
        "username": "heidi",
        "email": "heidi@example.com",
        "password": "password7",
    },
    {"username": "ivan", "email": "ivan@example.com", "password": "password8"},
    {"username": "judy", "email": "judy@example.com", "password": "password9"},
    {
        "username": "mallory",
        "email": "mallory@example.com",
        "password": "password10",
    },
    {
        "username": "oscar",
        "email": "oscar@example.com",
        "password": "password11",
    },
]


def seed_users(session):
    for user in users:
        db_user = Users(
            username=user["username"],
            email=user["email"],
            password=hash_password(user["password"]),
        )
        session.add(db_user)
    session.commit()
    return users
