# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
#
# Flask-Resources is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Loader module."""

from flask import request

from .context import resource_requestctx


class LoaderMixin:
    """Loader interface."""

    def load_item_request(self, *args, **kwargs):
        """Load a request concerning an existing item."""
        raise NotImplementedError()

    def load_create_request(self, *args, **kwargs):
        """Load an item creation request."""
        raise NotImplementedError()

    def load_search_request(self, *args, **kwargs):
        """Load a search request."""
        raise NotImplementedError()


class RequestLoader(LoaderMixin):
    """Loaded request representation.

    Loads the content from the request.
    """

    def __init__(self, deserializer=None, args_parser=None, *args, **kwargs):
        """Constructor."""
        self.deserializer = deserializer
        self.args_parser = args_parser

    def load_item_request(self, data=True, *args, **kwargs):
        """Build response headers."""
        if data:
            resource_requestctx.request_content = self.deserializer.deserialize_data(
                request.data
            )

    def load_create_request(self, *args, **kwargs):
        """Load an item creation request."""
        resource_requestctx.request_content = self.deserializer.deserialize_data(
            request.data
        )

    def load_search_request(self, *args, **kwargs):
        """Load a search request."""
        resource_requestctx.request_args = self.args_parser.parse()
