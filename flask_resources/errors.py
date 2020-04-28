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

# FIXME: (LARS) This has to be reviewed


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

        return json.dumps(body)

    def get_headers(self, environ=None):
        """Get a list of headers."""
        return [("Content-Type", "application/json")]


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
        super(SearchPaginationRESTError, self).__init__(
            errors=_errors, **kwargs
        )


# class InvalidContentType(RESTException):
#     """Error for when an invalid Content-Type is provided."""

#     code = 415
#     """HTTP Status code."""

#     def __init__(self, allowed_content_types=None, **kwargs):
#         """Initialize exception."""
#         super(InvalidContentType, self).__init__(**kwargs)
#         self.allowed_content_types = allowed_content_types
#         self.description = "Invalid 'Content-Type' header. Expected one of: {0}".format(
#             ", ".join(allowed_content_types)
#         )


# class RESTValidationError(RESTException):
#     """A standard REST validation error."""

#     code = 400
#     """HTTP Status code."""

#     description = "Validation error."
#     """Error description."""


# class SameContentException(RESTException):
#     """304 Same Content exception.

#     Exception thrown when request is GET or HEAD, ETag is If-None-Match and
#     one or more of the ETag values match.
#     """

#     code = 304
#     """HTTP Status code."""

#     description = "Same Content."
#     """Error description."""

#     def __init__(self, etag, last_modified=None, **kwargs):
#         """Constructor.

#         :param etag: matching etag
#         :param last_modified: The last modified date. (Default: ``None``)
#         """
#         super(SameContentException, self).__init__(**kwargs)
#         self.etag = etag
#         self.last_modified = last_modified

#     def get_response(self, environ=None):
#         """Get a list of headers."""
#         response = super(SameContentException, self).get_response(
#             environ=environ
#         )
#         if self.etag is not None:
#             response.set_etag(self.etag)
#         if self.last_modified is not None:
#             response.headers["Last-Modified"] = http_date(self.last_modified)
#         return response
