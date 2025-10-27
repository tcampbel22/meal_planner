from sqlmodel import Session, select
import uuid
from app.database.models import Users, Recipes
from typing import Optional


def delete_user(id: uuid.UUID, session: Session) -> Optional[Users]:
    user = session.get(Users, id)
    if user:
        session.delete(user)
        session.commit()
    return user


def get_all_users(session: Session) -> list[Users]:
    return session.exec(select(Users)).all()


def get_first_user(session: Session) -> Users:
    return session.exec(select(Users)).first()


def get_all_recipes(session: Session) -> list[Recipes]:
    return session.exec(select(Recipes)).all()


def get_users_length(session: Session) -> int:
    users = session.exec(select(Users)).all()
    return len(users)
