import redis

class Config:
    REDIS_HOST = 'localhost'
    REDIS_PORT = 6379
    REDIS_DB = 0
    USER_SESSION_TIMEOUT = 3600  # Thời gian hết hạn phiên user (1 giờ)

def get_redis_connection():
    return redis.Redis(
        host=Config.REDIS_HOST,
        port=Config.REDIS_PORT,
        db=Config.REDIS_DB,
        decode_responses=True
    )