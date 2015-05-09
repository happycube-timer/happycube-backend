from happycube.service import BaseService
from happycube.users.models import User


class UserService(BaseService):
    __model__ = User

user = UserService()


