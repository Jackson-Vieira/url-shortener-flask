import redis
import sys

import os

from dotenv import load_dotenv
from datetime import timedelta

load_dotenv()

def redis_connect() -> redis.client.Redis:
    try:
        client = redis.Redis(
            host=os.getenv("REDIS_HOST"),
            port=os.getenv("REDIS_PORT"),
            db=0,
            socket_timeout=5,
        )
        ping = client.ping()
        if ping is True:
            return client
    except redis.AuthenticationError:
        print("Redis AuthenticationError")
        sys.exit(1)

class Cache:
    def __init__(self, client: redis.client.Redis):
        self.client = client

    def get(self, key: str) -> str:
        """Get data from redis."""
        result = self.client.get(key)
        return result

    def set(self, key: str, value: str) -> bool:
        """Set data to redis."""
        state = self.client.setex(
            key,
            timedelta(days=15),
            value=value,
        )
        return state