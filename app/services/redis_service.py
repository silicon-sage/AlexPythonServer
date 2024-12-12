import redis
from redis.exceptions import RedisError

redis_client = None

def init_redis_client(app):
    global redis_client
    
    redis_config = app.config.get('redis', {})
    redis_client = redis.Redis(
        host=redis_config.get('host', 'localhost'),
        port=redis_config.get('port', 6379),
        db=redis_config.get('db', 0),
        username=redis_config.get('username'),
        password=redis_config.get('password'),
        ssl=redis_config.get('ssl', False),
        decode_responses=True,
        socket_timeout=redis_config.get('socket_timeout', 5),
        socket_connect_timeout=redis_config.get('socket_connect_timeout', 5),
        retry_on_timeout=redis_config.get('retry_on_timeout', True)
    )
    return redis_client

def get_redis_client():
    return redis_client