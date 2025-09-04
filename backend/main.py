from fastapi import FastAPI
from api.routes import user_routes

app = FastAPI()

app.include_router(user_routes.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/items/{id}")
async def read_item(id: int):
    return {"item_id": id}
