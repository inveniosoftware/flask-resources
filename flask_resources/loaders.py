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

    def load_item_request(self, *args, **kwargs):
        """Build response headers."""
        {"request_content": self.deserializer.deserialize_data(request.data)}

    def load_search_request(self, *args, **kwargs):
        """Load a search request."""
        {"request_args": self.args_parser.parse()}
