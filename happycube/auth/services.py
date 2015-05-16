from happycube.errors import HTTPError
from happycube.users.models import User
from flask import g, request
import jwt


def get_authenticated_user(login, password):
    user = User.first(name=login)
    if user and user.check_password(password):
        return user
    else:
        return None


def name_available(login):
    user = User.first(name=login)
    if user is None:
        return True
    else:
        return False


def register_new_user(login, password):
    return User.create(name=login, password=password)


def verify_jwt():
    """Does the actual work of verifying the JWT data in the current request.
    """
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
        g.user = User.get(payload.get('user_id'))
    except:
        raise HTTPError(401, 'User does not exist')

    return None


def issue_jwt(user):
    return jwt.encode({'user_id': user.id}, 'secret')
