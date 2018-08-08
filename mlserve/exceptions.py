import json
from aiohttp import web
from typing import Optional, Dict, Any


# Server related exceptions
class RESTError(web.HTTPError):  # type: ignore
    status_code = 500
    error = 'Unknown Error'

    def __init__(
        self: 'RESTError',
        message: Optional[str] = None,
        status_code=Optional[int],
        *args: Any,
        **kwargs: Any
    ) -> None:
        super().__init__(reason=message)

        if status_code is not None:
            self.status_code = status_code

        if not message:
            message = self.error

        msg_dict: Dict[str, Any] = {'error': message}

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
    def status_code(self) -> int:
        r: int = self.args[0]
        return r


class PlainRestError(RestClientError):
    """Answer is not JSON, for example for 500 Internal Server Error"""

    @property
    def error_text(self) -> str:
        return str(self.args)
