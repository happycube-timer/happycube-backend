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

from happycube.solves.services import solve_service
from happycube.solves.serializer import serialize

import json

blueprint = Blueprint('solves', __name__,  url_prefix='/api/v0/solves')

@blueprint.route('/', methods = ['GET'])
@jwt_required()
def index():

    solves = solve_service.all()

    ret = [serialize(x) for x in solves]

    return json.dumps(ret)


@blueprint.route('/', methods = ['POST'])
@jwt_required()
def create():
    logger.info(request.get_json())

    payload = request.get_json()
    payload['user_id'] = g.user.id

    new_solve = solve_service.create(**payload)

    return json.dumps(serialize(new_solve))

