import jwt

from functools import wraps
from flask import request, g

from happycube.log import logger
from happycube.errors import HTTPError

from happycube.users.services import user


def jwt_required(debug=False):
    """View decorator that requires a valid JWT token to be present in the request
    :param realm: an optional realm
    """
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt(debug)
            return fn(*args, **kwargs)
        return decorator
    return wrapper

# from happycube.users.services import get_user

def verify_jwt(debug):
    """Does the actual work of verifying the JWT data in the current request.
    """
    if debug:
        g.user = user.get('1')
        return

    auth = request.headers.get('Authorization', None)

    if auth is None:
        raise HTTPError(401, 'Authorization header was missing')

    segments = auth.split()

    if segments[0].lower() != 'bearer':
        raise HTTPError(401, 'Authorization header format is \'Bearer TOKEN\'')
    elif len(segments) == 1:
        raise HTTPError(401, 'Token missing')
    elif len(segments) > 2:
        raise HTTPError(401, 'Token invalid')

    try:
        payload = jwt.decode(segments[1], 'secret') # TODO: make secret key secret
    except jwt.ExpiredSignatureError:
        raise HTTPError(401, 'Token expired')
    except jwt.DecodeError:
        raise HTTPError(401, 'Token invalid')

    try:
        g.user = user.get('user_id')
    except:
        raise HTTPError(401, 'User does not exist')

    return None
