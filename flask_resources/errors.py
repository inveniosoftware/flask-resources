# -*- coding: utf-8 -*-
#
# Copyright (C) 2020-2021 CERN.
# Copyright (C) 2020-2021 Northwestern University.
#
# Flask-Resources is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Exceptions used in Flask Resources module."""

import json

from flask import current_app, g
from werkzeug.exceptions import HTTPException

from .serializers.json import JSONEncoder


def create_error_handler(map_func_or_exception):
    """Creates a resource error handler.

    The handler is used to map business logic exceptions to
    REST exceptions. The original exceptions is being stored
    in the `__original_exc__` attribute of the mapped exception.

    :param map_func_or_exception: Function or exception to map originally
        raised exception to a `flask_resources.errors.HTTPJSONException`.
    """

    def error_handler(e):
        if isinstance(e, HTTPJSONException):
            mapped_exc = e
        elif isinstance(map_func_or_exception, HTTPJSONException):
            mapped_exc = map_func_or_exception
        else:
            mapped_exc = map_func_or_exception(e)
        mapped_exc.__original_exc__ = e
        current_app.logger.debug(
            "A resource error handler caught the following exception:", exc_info=True
        )
        return mapped_exc.get_response()

    return error_handler


handle_http_exception = create_error_handler(
    lambda exc: HTTPJSONException(code=exc.code, description=exc.description)
)


class HTTPJSONException(HTTPException):
    """HTTP Exception delivering JSON error responses."""

    errors = None

    def __init__(self, code=None, errors=None, **kwargs):
        """Initialize HTTPJSONException."""
        super(HTTPJSONException, self).__init__(**kwargs)
        if errors is not None:
            self.errors = errors
        if code is not None:
            self.code = code

    @property
    def name(self):
        """The status name."""
        return type(self).__name__

    def get_errors(self):
        """Get errors.

        :returns: A list containing the errors.
        """
        return [e for e in self.errors] if self.errors else None

    def get_description(self, environ=None, scope=None):
        """Returns an unescaped description."""
        return self.description

    def get_headers(self, environ=None, scope=None):
        """Get a list of headers."""
        return [("Content-Type", "application/json")]

    def get_body(self, environ=None, scope=None):
        """Get the request body."""
        body = {"status": self.code, "message": self.get_description(environ)}

        errors = self.get_errors()
        if errors:
            body["errors"] = errors

        # TODO: Revisit how to integrate error monitoring services. See issue #56
        # Temporarily kept for expediency and backward-compatibility
        if self.code and (self.code >= 500) and hasattr(g, "sentry_event_id"):
            body["error_id"] = str(g.sentry_event_id)

        return json.dumps(body, cls=JSONEncoder)


class MIMETypeException(HTTPJSONException):
    """Error for when an invalid Content-Type is provided."""

    header_name = None

    def __init__(self, allowed_mimetypes=None, **kwargs):
        """Initialize exception."""
        super(MIMETypeException, self).__init__(**kwargs)
        self.allowed_mimetypes = allowed_mimetypes
        self.description = "Invalid '{0}' header. Expected one of: {1}".format(
            self.header_name, ", ".join(allowed_mimetypes)
        )


class MIMETypeNotAccepted(MIMETypeException):
    """Error for when an invalid `Accept` header is provided."""

    code = 406
    header_name = "Accept"


class InvalidContentType(MIMETypeException):
    """Error for when an invalid `Content-Type` header is provided."""

    code = 415
    header_name = "Content-Type"
