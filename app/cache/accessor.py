import redis

def get_redis_connection() -> redis.Redis:
    return redis.Redis(
        host="localhost",
        port=6379,
        db=0
    )


def set_product():
    redis = get_redis_connection()
    redis.set("product", 1)

def get_product():
    redis = get_redis_connection()
    return redis.get("product")