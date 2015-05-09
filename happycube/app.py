# -*- coding: utf-8 -*-
'''The app module, containing the app factory function.'''
from flask import Flask, jsonify, g

from happycube.settings import ProdConfig

from happycube.extensions import (
    bcrypt,
    cache,
    debug_toolbar,
    db,
    # admin,
)

from happycube import users, solves
from happycube.errors import HTTPError
# from happycube.database import db
from happycube.log import logger


def create_app(config_object=ProdConfig):
    '''An application factory, as explained here:
        http://flask.pocoo.org/docs/patterns/appfactories/

    :param config_object: The configuration object to use.
    '''
    app = Flask(__name__)
    app.config.from_object(config_object)
    register_extensions(app)
    register_blueprints(app)
    register_errorhandlers(app)
    register_events(app)
    # register_logger(app)
    return app


def register_extensions(app):
    # assets.init_app(app)
    # bcrypt.init_app(app)
    # cache.init_app(app) # uncomment to enable caching
    db.init_app(app)
    debug_toolbar.init_app(app)
    # admin.init_app(app)
    # admin.add_view(OrderAdmin(Order))
    # migrate.init_app(app, db)
    # redis.init_app(app)
    return None


def register_blueprints(app):
    app.register_blueprint(users.views.blueprint)
    app.register_blueprint(solves.views.blueprint)
    return None


def register_errorhandlers(app):

    # Errors thrown by happycube
    @app.errorhandler(HTTPError)
    def http_error(error):
        return jsonify(error.to_dict()), error.code

    # @app.errorhandler(403)
    # def forbidden(error):
    #     return jsonify( { 'error': 'Forbidden' } ), 403


    # Errors thrown by Flask/Werkzeug
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'error': 'Bad request',
            'message': 'The server could not understand the request'
        }), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'error': 'Not found',
            'message': 'The requested resource was not found on the server'
        }), 404

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            'error': 'Method not allowed',
            'message': 'The requested resource did not accept the HTTP method used'
        }), 405


def register_events(app):
    # @app.before_request
    # def before_request():
    #     # logger.info('before')
    #     g.db = db
    #     g.db.connect()

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Content-Type', 'application/json')

        return response

# def register_logger(app):
#     handler = RotatingFileHandler('foo.log', maxBytes=10000, backupCount=1)
#     handler.setLevel(logging.DEBUG)
#     app.logger.addHandler(handler)
