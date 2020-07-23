# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
# Copyright (C) 2020 Northwestern University.
#
# Flask-Resources is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Loader module."""

from functools import wraps

from flask import request

from .context import resource_requestctx
from .errors import InvalidContentType


def select_deserializer(resource_method, loader_or_loaders):
    """Returns deserializer corresponding to situation."""
    if isinstance(loader_or_loaders, RequestLoader):
        return loader_or_loaders.deserializer

    loader = loader_or_loaders.get(resource_method)
    if loader:
        return loader.deserializer
    else:
        raise InvalidContentType(allowed_mimetypes=loader_or_loaders.keys())


def request_loader(f):
    """Decorator that loads/deserializes the request data."""

    @wraps(f)
    def wrapper(self, *args, **kwargs):
        """Wrapping method.

        :params self: Item/List/SingletonView instance
        """
        # Checking Content-Type is the responsibility of the loader
        loaders = self.resource.config.request_loaders

        request_content_type = request.content_type

        if not request_content_type:
            request_content_type = self.resource.config.default_content_type

        if request_content_type not in loaders:
            raise InvalidContentType(allowed_mimetypes=loaders.keys())

        deserializer = select_deserializer(
            self.resource_method, loaders[request_content_type]
        )

        resource_requestctx.request_content = deserializer.deserialize_data(
            request.data
        )

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
