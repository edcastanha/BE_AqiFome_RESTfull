import redis
import os

class RedisConfig:
    def __init__(self):
        self.host = os.getenv("REDIS_HOST", "localhost")
        self.port = int(os.getenv("REDIS_PORT", 6379))
        self.db = int(os.getenv("REDIS_DB", 0))
        self.decode_responses = True
        self.expires = int(os.getenv("REDIS_EXPIRATION", 3600))

    def get_client(self):
        return redis.Redis(
            host=self.host,
            port=self.port,
            db=self.db,
            decode_responses=self.decode_responses
        )

    def get_expires(self):
        return self.expires
