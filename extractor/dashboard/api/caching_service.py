import redis
import json

# Initialize Redis connection
cache = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)

def get_cached_data(keyword):
    """Retrieve cached sentiment data."""
    data = cache.get(keyword)
    return json.loads(data) if data else None

def cache_data(keyword, data, expiry=3600):
    """Store sentiment data in Redis for faster access."""
    cache.setex(keyword, expiry, json.dumps(data))
