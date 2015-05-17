# -*- coding: utf-8 -*-
'''Public section, including homepage and signup.'''
from flask import (Blueprint, request, render_template, flash, url_for,
                    redirect, session, jsonify, abort, g)

from happycube.extensions import cache
from happycube.errors import HTTPError
from happycube.log import logger

from happycube.decorators.validation import validate
from happycube.decorators.rate_limit import limit
from happycube.decorators.auth import jwt_required

from .services import get_all_solves, create_solve
from .serializer import serialize

import json

blueprint = Blueprint('solves', __name__,  url_prefix='/api/v0/solves')

@blueprint.route('/', methods = ['GET'])
@jwt_required()
def index():

    solves = get_all_solves(g.user.id)

    ret = [serialize(x) for x in solves]

    return json.dumps(ret)


@blueprint.route('/', methods = ['POST'])
@jwt_required()
def create():
    payload = request.get_json()

    new_solve = create_solve(
        user_id=g.user.id,
        scramble=payload['scramble'],
        ellapsed_time=payload['ellapsed_time']
    )

    return json.dumps(serialize(new_solve))

