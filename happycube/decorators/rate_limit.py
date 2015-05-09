from functools import wraps
from flask import request, abort

from happycube.database import redis_connection
from happycube.errors import HTTPError


def limit(requests=2, window=10):
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            key = "rl:{}".format(request.remote_addr)

            try:
                remaining = requests - int(redis_connection.get(key))
            except (ValueError, TypeError):
                remaining = requests
                redis_connection.set(key, 0)

            ttl = redis_connection.ttl(key)
            if not ttl:
                redis_connection.expire(key, window)
                ttl = window

            if remaining > 0:
                redis_connection.incr(key, 1)
                return f(*args, **kwargs)
            else:
                raise HTTPError(429, 'You have exceeded the allowed amount of requests')
        return wrapped
    return decorator
