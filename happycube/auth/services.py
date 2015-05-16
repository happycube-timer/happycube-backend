from happycube.service import BaseService
from happycube.users.services import user_service
from happycube.errors import HTTPError
from flask import g, request
import jwt


class AuthService(object):

    def get_authenticated_user(self, login, password):
        user = user_service.first(name=login)
        if user and user.check_password(password):
            return user
        else:
            return None


    def verify_jwt(self):
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
            g.user = user_service.get(payload.get('user_id'))
        except:
            raise HTTPError(401, 'User does not exist')

        return None


    def issue_jwt(self, user):
        return jwt.encode({'user_id': user.id}, 'secret')


auth_service = AuthService()
