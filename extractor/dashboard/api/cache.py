import time
import json
import hashlib

cache_store = {}

def generate_cache_key(params: dict) -> str:
    """Generates a unique cache key based on request parameters."""
    hash_input = json.dumps(params, sort_keys=True)
    return hashlib.md5(hash_input.encode()).hexdigest()

def cache_result(func):
    """Decorator to cache API responses for faster retrieval."""
    def wrapper(*args, **kwargs):
        cache_key = generate_cache_key(kwargs)
        if cache_key in cache_store and time.time() - cache_store[cache_key]['timestamp'] < 300:
            return cache_store[cache_key]['data']
        
        result = func(*args, **kwargs)
        cache_store[cache_key] = {"data": result, "timestamp": time.time()}
        return result
    return wrapper
