from happycube.solves.models import Solve

def get_all_solves(user_id):
    return Solve.find(user_id=user_id)

def create_solve(**kwargs):
    return Solve.create(**kwargs)
