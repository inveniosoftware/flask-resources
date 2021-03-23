# -*- coding: utf-8 -*-
#
# Copyright (C) 2020-2021 CERN.
# Copyright (C) 2020-2021 Northwestern University.
#
# Flask-Resources is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Response module."""

from functools import wraps

from flask import Response, make_response

from .context import resource_requestctx


def response_handler(many=False):
    """Decorator for using the response handler to create the HTTP response.

    The response handler works in conjunction with ``with_content_negotiation()``
    which is responsible for selecting the correct response handler based on
    the content negotiation.

    .. code-block:: python

        @response_handler()
        def read(self):
            return obj, 200

        @response_handler(many=True)
        def search(self):
            return [obj], 200
    """

    def decorator(f):
        @wraps(f)
        def inner(*args, **kwargs):
            res = f(*args, **kwargs)
            return resource_requestctx.response_handler.make_response(*res, many=many)

        return inner

    return decorator


class ResponseHandler:
    """Response handler which delegates to the a serializer.

    Example usage:

    .. code-block:: python

        def obj_headers(obj_or_list, code, many=False):
            return {'etag': ... }

        class Config(ResourceConfig):
            response_handlers = {
                "application/json": ResponseHandler(
                    JSONSerializer(), headers=obj_headers)
            }
    """

    def __init__(self, serializer, headers=None):
        """Constructor."""
        self.serializer = serializer
        self.headers = headers

    def make_headers(self, obj_or_list, code, many=False):
        """Builds the headers fo the response."""
        if self.headers is None:
            return {
                "content-type": resource_requestctx.accept_mimetype,
            }
        elif callable(self.headers):
            return self.headers(obj_or_list, code, many=many)
        else:
            return self.headers

    def make_response(self, obj_or_list, code, many=False):
        """Builds a response for one object."""
        # If view returns a response, bypass the serialization.
        if isinstance(obj_or_list, Response):
            return obj_or_list

        # https://flask.palletsprojects.com/en/1.1.x/api/#flask.Flask.make_response
        # (body, status, header)
        if many:
            serialize = self.serializer.serialize_object_list
        else:
            serialize = self.serializer.serialize_object

        return make_response(
            "" if obj_or_list is None else serialize(obj_or_list),
            code,
            self.make_headers(obj_or_list, code, many=many),
        )
