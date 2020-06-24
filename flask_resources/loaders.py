# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
#
# Flask-Resources is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Loader module."""

from functools import wraps

from flask import request
from werkzeug.exceptions import UnsupportedMediaType

from .context import resource_requestctx


def request_loader(f):
    """Decorator that sets the request_loader on the view."""

    @wraps(f)
    def wrapper(self, *args, **kwargs):
        """Wrapping method.

        :params self: ItemView or ListView class
        """
        # Checking Content-Type is the responsibility of the deserializer/loader
        loaders = self.resource.config.request_loaders

        if request.content_type not in loaders:
            raise UnsupportedMediaType()

        self.request_loader = loaders[request.content_type]

        return f(self, *args, **kwargs)

    return wrapper


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
        return {"request_content": self.deserializer.deserialize_data(request.data)}

    def load_search_request(self, *args, **kwargs):
        """Load a search request."""
        return {"request_args": self.args_parser.parse()}
