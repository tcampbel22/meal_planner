from fastapi import APIRouter

router = APIRouter()


@router.get("/user/{id}")
async def get_user(id: int):
    return {"user": "Bob", "id:": id}
