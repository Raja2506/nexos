import redis
from fastapi import Request, HTTPException

# Same Redis your project already uses (Day 4 setup)
redis_client = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)

RATE_LIMIT = 20        # max requests allowed
WINDOW_SECONDS = 60    # per 60 seconds

async def rate_limit_dependency(request: Request):
    identifier = request.client.host   # IP-based for now

    key = f"rate_limit:{identifier}"
    current = redis_client.incr(key)

    if current == 1:
        redis_client.expire(key, WINDOW_SECONDS)

    if current > RATE_LIMIT:
        raise HTTPException(status_code=429, detail="Too many requests. Slow down.")

    return True