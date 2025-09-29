from redis import asyncio as aioredis
import os

REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379")
redis_client = aioredis.from_url(REDIS_URL, decode_responses=True)


async def start_redis():
    try:
        await redis_client.ping()
        print("Connected to Redis!")
    except Exception as e:
        print("Redis connection failed:", e)
        raise e


async def close_redis():
    await redis_client.close()
