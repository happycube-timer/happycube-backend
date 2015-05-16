from functools import wraps
from happycube.auth.services import auth_service

def jwt_required():
    """View decorator that requires a valid JWT token to be present in the request
    :param realm: an optional realm
    """
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            auth_service.verify_jwt()
            return fn(*args, **kwargs)
        return decorator
    return wrapper

