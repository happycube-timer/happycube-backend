from happycube.service import BaseService
from happycube.solves.models import Solve


class SolveService(BaseService):
    __model__ = Solve

solve_service = SolveService()


