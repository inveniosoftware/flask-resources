# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
#
# Flask-Resources is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Exceptions used in Flask Resources module."""

import json

from flask import g
from werkzeug.exceptions import HTTPException
from werkzeug.http import http_date


class RESTException(HTTPException):
    """HTTP Exception delivering JSON error responses."""

    errors = None

    def __init__(self, errors=None, **kwargs):
        """Initialize RESTException."""
        super(RESTException, self).__init__(**kwargs)
        if errors is not None:
            self.errors = errors

    def get_errors(self):
        """Get errors.

        :returns: A list containing a dictionary representing the errors.
        """
        return [e.to_dict() for e in self.errors] if self.errors else None

    def get_description(self, environ=None):
        """Get the description."""
        return self.description

    def get_body(self, environ=None):
        """Get the request body."""
        body = dict(status=self.code, message=self.get_description(environ),)

        errors = self.get_errors()
        if self.errors:
            body["errors"] = errors

        if self.code and (self.code >= 500) and hasattr(g, "sentry_event_id"):
            body["error_id"] = str(g.sentry_event_id)

        return body


#
# Loading/Serializing
#
class UnsupportedMimetypeError(RESTException):
    """The request content or accepts a MIMEType that the application cannot serialize.

    It applies to both `Content-Type` and `Accept` headers. Potentially to any other
    passed as the `header` parameter.
    """

    code = 415

    def __init__(self, header, received_mimetype, allowed_mimetypes, *args, **kwargs):
        """Initialize exception."""
        super(UnsupportedMimetypeError, self).__init__(*args, **kwargs)
        self.description = (
            "Invalid '{}' header. "
            "Received '{}'. Expected one of: {}".format(
                header, received_mimetype, ", ".join(allowed_mimetypes)
            )
        )


# FIXME: From here down need review


class FieldError(object):
    """Represents a field level error.

    .. note:: This is not an actual exception.
    """

    def __init__(self, field, message, code=None):
        """Init object.

        :param field: Field name.
        :param message: The text message to show.
        :param code: The HTTP status to return. (Default: ``None``)
        """
        self.res = dict(field=field, message=message)
        if code:
            self.res["code"] = code

    def to_dict(self):
        """Convert to dictionary.

        :returns: A dictionary with field, message and, if initialized, the
            HTTP status code.
        """
        return self.res


#
# Search
#
class SearchPaginationRESTError(RESTException):
    """Search pagination error."""

    code = 400

    def __init__(self, errors=None, **kwargs):
        """Initialize exception."""
        _errors = []
        if errors:
            for field, messages in errors.items():
                _errors.extend([FieldError(field, msg) for msg in messages])
        super(SearchPaginationRESTError, self).__init__(errors=_errors, **kwargs)
