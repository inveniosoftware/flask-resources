# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
#
# Flask-Resources is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Loader module."""

from flask import request


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
        create_args_parser=None,
        search_args_parser=None,
        *args,
        **kwargs
    ):
        """Constructor."""
        self.deserializer = deserializer
        self.item_args_parser = item_args_parser
        self.create_args_parser = create_args_parser
        self.search_args_parser = search_args_parser

    def load_item_request(self, *args, **kwargs):
        """Build response headers."""
        return (
            self.item_args_parser.parse(),
            self.deserializer.deserialize_object(request.data),
        )

    def load_create_request(self, *args, **kwargs):
        """Load an item creation request."""
        return (
            self.create_args_parser.parse(),
            self.deserializer.deserialize_object(request.data),
        )

    def load_search_request(self, *args, **kwargs):
        """Load a search request."""
        return self.search_args_parser.parse()
