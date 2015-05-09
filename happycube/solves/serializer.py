def serialize(solve):
    return {
        'id': solve.id,
        'user_id': solve.user.id,
        'scramble': solve.scramble,
        'ellapsed_time': solve.ellapsed_time
    }
