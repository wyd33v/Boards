import json

import redis

from config import Config


class CacheService:
    _client = None
    
    def __init__(self):
        if self._client is None:
            # Connect to Redis
            self._client = redis.Redis(host="localhost", port=Config.CACHE_PORT, db=0)

    def set_value(self, key:str , value, exp: int = -1):
        value_json = json.dumps(value, ensure_ascii=False, indent=2)
        if exp > 0:
            self._client.set(key, value_json, exp)
        else:
            self._client.set(key, value_json)

    def get_value(self, key: str):
        value_json = self._client.get(key)
        if value_json is None:
            raise KeyError("cache: no key is found")
        value = json.loads(value_json)
        return value

    def get_process(self, req_id: str):
        process_cache_key = f"process:{req_id}"
        return self.get_value(process_cache_key)
