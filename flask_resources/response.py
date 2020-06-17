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

    def make_header(self, content=None):
        """Build response headers."""
        return {
            "content-type": resource_requestctx.payload_mimetype,
            "accept": resource_requestctx.accept_mimetype,
        }

    def make_response(self, code, content):
        """Builds a response."""
        raise NotImplementedError()

    def make_error_response(self, error):
        """Builds an error response."""
        raise NotImplementedError()


class ItemResponse(ResponseMixin):
    """Item response representation.

    Builds up a reponse for a single object.
    """

    def __init__(self, serializer=None, *args, **kwargs):
        """Constructor."""
        self.serializer = serializer

    def make_response(self, code, content):
        """Builds a response for a single object."""
        # https://flask.palletsprojects.com/en/1.1.x/api/#flask.Flask.make_response
        # (body, status, header)

        return make_response(
            self.serializer.serialize_object(content), code, self.make_header(),
        )

    def make_error_response(self, error):
        """Builds an error response."""
        return make_response(
            self.serializer.serialize_error(error), error.code, self.make_header()
        )


class ListResponse(ResponseMixin):
    """List response representation.

    Builds up a reponse for a list of objects.
    """

    def __init__(self, serializer=None, *args, **kwargs):
        """Constructor."""
        self.serializer = serializer

    def make_response(self, code, content):
        """Builds a response for a list of objects."""
        # https://flask.palletsprojects.com/en/1.1.x/api/#flask.Flask.make_response
        # (body, status, header)

        return make_response(
            self.serializer.serialize_object_list(content), code, self.make_header(),
        )

    def make_error_response(self, error):
        """Builds an error response."""
        # FIXME: Repeated code with above. Is there a chance of having a
        # Response w/o a serializer? If not this can refactor on parent mixin.
        return make_response(
            self.serializer.serialize_error(error), error.code, self.make_header()
        )
