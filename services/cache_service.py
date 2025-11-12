import redis

from config import Config

# Connect to Redis
redis_client = redis.Redis(host='localhost', port=Config.CACHE_PORT, db=0)


count_key_name = "test_key"

def set_count(value:int, exp:int=-1):
    if exp > 0:
        redis_client.set(count_key_name, value, exp)
    else:
        redis_client.set(count_key_name, value)

def get_cout():
    value = redis_client.get(count_key_name)
    return value

