# -*- coding: utf-8 -*-
'''Public section, including homepage and signup.'''
from flask import (Blueprint, request, render_template, flash, url_for,
                    redirect, session, jsonify, abort, g)

from happycube.extensions import cache
from happycube.errors import HTTPError
from happycube.log import logger

from happycube.decorators.validation import validate
from happycube.decorators.rate_limit import limit

from happycube.auth.services import (
    get_authenticated_user,
    issue_jwt,
    name_available,
    register_new_user
)

blueprint = Blueprint('auth', __name__,  url_prefix='/api/v0/auth')

@blueprint.route('/login/', methods = ['POST'])
def login():
    payload = request.get_json()
    user = get_authenticated_user(payload['login'], payload['password'])

    if user:
        token = issue_jwt(user)
        ret = {
            'token': token.decode('utf-8')
        }

        return jsonify(ret)
    else:
        raise HTTPError(401, 'Login failed')


@blueprint.route('/sign-up/', methods = ['POST'])
def sign_up():
    payload = request.get_json()
    if name_available(payload['login']):
        register_new_user(payload['login'], payload['password'])

        ret = {}

        return jsonify(ret)
    else:
        raise HTTPError(403, 'Username already exists')


@blueprint.route('/logout/', methods = ['POST'])
def logout():

    ret = {
        'message': 'Logout successful'
    }

    return jsonify(ret)
