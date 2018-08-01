import json
from aiohttp import web


# Server related exceptions
class RESTError(web.HTTPError):
    status_code = 500
    error = 'Unknown Error'

    def __init__(self, message=None, status_code=None, **kwargs):
        super().__init__(reason=message)

        if status_code is not None:
            self.status_code = status_code

        if not message:
            message = self.error

        msg_dict = {'error': message}

        if kwargs:
            msg_dict['error_details'] = kwargs

        self.text = json.dumps(msg_dict)
        self.content_type = 'application/json'


class ObjectNotFound(RESTError):
    status_code = 404
    error = 'Object not found'


class UnprocessableEntity(RESTError):
    status_code = 422
    error = 'Unprocessable Entity'


# REST client related exceptions
class RestClientError(Exception):
    """Base exception class for RESTClient"""

    @property
    def status_code(self):
        return self.args[0]


class PlainRestError(RestClientError):
    """Answer is not JSON, for example for 500 Internal Server Error"""

    @property
    def error_text(self):
        return self.args[1]
