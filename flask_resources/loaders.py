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

    def __init__(
        self,
        deserializer=None,
        item_args_parser=None,
        search_args_parser=None,
        *args,
        **kwargs
    ):
        """Constructor."""
        self.deserializer = deserializer
        self.item_args_parser = item_args_parser
        self.search_args_parser = search_args_parser

    def load_item_request(self, data=True, *args, **kwargs):
        """Build response headers."""
        resource_requestctx.request_args = self.item_args_parser.parse()
        if data:
            resource_requestctx.request_content = self.deserializer.deserialize_object(
                request.data
            )

    def load_create_request(self, *args, **kwargs):
        """Load an item creation request."""
        resource_requestctx.request_content = self.deserializer.deserialize_object(
            request.data
        )

    def load_search_request(self, *args, **kwargs):
        """Load a search request."""
        resource_requestctx.request_args = self.search_args_parser.parse()