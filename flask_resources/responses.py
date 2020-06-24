# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
#
# Flask-Resources is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Response module."""

from flask import make_response

from .context import resource_requestctx


class ResponseMixin:
    """Response interface."""

    def make_headers(self, content=None):
        """Build response headers."""
        return {"content-type": resource_requestctx.payload_mimetype}

    def make_item_response(self, content, code):
        """Builds a response."""
        raise NotImplementedError()

    def make_list_response(self, content, code):
        """Builds a response."""
        raise NotImplementedError()

    def make_error_response(self, error):
        """Builds an error response."""
        raise NotImplementedError()


class Response(ResponseMixin):
    """Response implementation.

    Builds up a reponse for a single or list of objects.
    """

    def __init__(self, serializer=None):
        """Constructor."""
        self.serializer = serializer

    def make_item_response(self, content, code=200):
        """Builds a response for a single object."""
        # https://flask.palletsprojects.com/en/1.1.x/api/#flask.Flask.make_response
        # (body, status, header)

        return make_response(
            self.serializer.serialize_object(content), code, self.make_headers(),
        )

    def make_list_response(self, content, code=200):
        """Builds a response for a list of objects."""
        # https://flask.palletsprojects.com/en/1.1.x/api/#flask.Flask.make_response
        # (body, status, header)

        return make_response(
            self.serializer.serialize_object_list(content), code, self.make_headers(),
        )

    def make_error_response(self, error):
        """Builds an error response."""
        return make_response(
            self.serializer.serialize_error(error), error.code, self.make_headers(),
        )
