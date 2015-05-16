from happycube.solves.models import Solve

def get_all_solves():
    return Solve.all()

def create_solve(payload):
    Solve.create(**payload)
