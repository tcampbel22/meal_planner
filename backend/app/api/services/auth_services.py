from app.database.models import Users
from app.database.database import SessionDep
from app.api.schemas.auth_schemas import LoginUser
import bcrypt


async def authenticate_user(user: LoginUser, session: SessionDep):
    data = session.get(Users, user.username)
    if not data:
        return 404
    validate = bcrypt.checkpw(user.password.encode("utf-8"), data.password)
    if not validate:
        return 400
    return 0
