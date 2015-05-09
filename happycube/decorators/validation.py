from functools import wraps
from flask import request, abort, jsonify
from werkzeug.exceptions import BadRequest


def validate_request(json, schema_name):
    # TODO: validate stuff
    pass


def validate(schema_name):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kw):
            try:
                request.json
            except BadRequest:
                abort(400, 'Payload must be a valid JSON')

            try:
                validate_request(request.get_json(), schema_name)
            except ValidationError:
                abort(400, 'Invalid parameters')

            return f(*args, **kw)
        return wrapper
    return decorator
