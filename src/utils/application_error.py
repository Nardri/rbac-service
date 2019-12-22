"""Module for Validation error and error handler"""


class ApplicationError(Exception):
    """Base Validation class for handling validation errors"""
    status_code = 400

    def __init__(self, errors, status_code=None, payload=None):
        Exception.__init__(self)
        self.errors = errors
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        """
        Returns:
        """

        rv = dict(self.payload or ())
        rv['status'] = 'error'
        rv['error'] = self.errors
        return rv, self.status_code
