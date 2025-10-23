from redis import asyncio as aioredis
from fastapi.requests import Request
import os


async def start_redis() -> aioredis.Redis:
    ENV = os.getenv("ENV")
    if ENV != "dev":
        REDIS_URL = "redis://redis_test:6379"
    else:
        REDIS_URL = "redis://redis_dev:6379"
    try:
        redis_client = aioredis.from_url(REDIS_URL, decode_responses=True)
        await redis_client.ping()
        print("Connected to Redis!")
        return redis_client
    except Exception as e:
        print("Redis connection failed:", e)
        raise e


async def close_redis(redis_client: aioredis.Redis) -> None:
    if redis_client:
        await redis_client.aclose()


def get_redis(request: Request):
    return request.app.state.redis
