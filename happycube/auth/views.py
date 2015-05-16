# -*- coding: utf-8 -*-
'''Public section, including homepage and signup.'''
from flask import (Blueprint, request, render_template, flash, url_for,
                    redirect, session, jsonify, abort, g)

from happycube.extensions import cache
from happycube.errors import HTTPError
from happycube.log import logger

from happycube.decorators.validation import validate
from happycube.decorators.rate_limit import limit

from happycube.auth.services import auth_service

blueprint = Blueprint('auth', __name__,  url_prefix='/api/v0/auth')

@blueprint.route('/login/', methods = ['POST'])
def login():
    payload = request.get_json()
    user = auth_service.get_authenticated_user(payload['login'], payload['password'])
    token = auth_service.issue_jwt(user)
    ret = {
        'token': token.decode('utf-8')
    }

    return jsonify(ret)
