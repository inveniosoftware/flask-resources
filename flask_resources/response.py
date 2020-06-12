# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
#
# Flask-Resources is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Response module."""

from flask import make_response


class ResponseMixin:
    """Response interface."""

    def make_response(code, content):
        """Builds a response."""
        raise NotImplementedError()

    def make_error_response(reason, message):
        """Builds an error response."""
        raise NotImplementedError()


class ItemResponse(ResponseMixin):
    """Item response representation.

    Builds up a reponse for a single object.
    """

    def __init__(self, serializer=None, *args, **kwargs):
        """Constructor."""
        self.serializer = serializer

    def make_response(code, content):
        """Builds a response for a single object."""
        # This should do the link building (e.g. sign posting): self, pagination, query, etc.
        # In case of list responses, it would also take care of extras such as aggregation
        make_response(
            body=self.serializer.serialize_object(content),  # content is the object
            status=code,
            headers=self.make_header(),
        )


class ListResponse(ResponseMixin):
    """List response representation.

    Builds up a reponse for a list of objects.
    """

    def __init__(self, serializer=None, *args, **kwargs):
        """Constructor."""
        self.serializer = serializer

    def make_response(code, content):
        """Builds a response for a list of objects."""
        # This should do the link building (e.g. sign posting): self, pagination, query, etc.
        # In case of list responses, it would also take care of extras such as aggregation
        make_response(
            body=self.serializer.serialize_object(content),  # content is the object
            response_code=code,
            headers=self.make_header(),
        )
