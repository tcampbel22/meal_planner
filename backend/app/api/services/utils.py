from app.database.database import SessionDep
from sqlalchemy import select
from app.database.models import Users


async def get_user_by_email(email: str, session: SessionDep):
    query = select(Users).where(Users.email == email)
    return session.exec(query).scalar_one_or_none()
