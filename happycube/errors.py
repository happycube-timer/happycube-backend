class HTTPError(Exception):
    ERRORS = {
        '400': 'Bad request',
        '401': 'Unauthorized',
        '403': 'Forbidden',
        '404': 'Not found',
        '405': 'Method not allowed',
        '429': 'Too many requests',
        '500': 'Internal server error'
    }


    def __init__(self, code, message='', payload=None):
        Exception.__init__(self)
        self.error = self.ERRORS[str(code)]
        self.message = message
        self.code = code
        # self.payload = payload

    def to_dict(self):
        # rv = dict(self.payload or ())
        rv = {}
        rv['error'] = self.error
        rv['message'] = self.message
        # rv['payload'] = self.payload
        return rv
