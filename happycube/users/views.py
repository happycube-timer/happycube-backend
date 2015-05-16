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

blueprint = Blueprint('users', __name__,  url_prefix='/api/v0')

@blueprint.route('/me/', methods = ['POST'])
@jwt_required(debug=True)
def get_balance():

    ret = {
        'id': g.user.id,
        'name': g.user.name,
        'created_at': g.user.created_at,
        'updated_at': g.user.updated_at
    }

    return jsonify(ret)
