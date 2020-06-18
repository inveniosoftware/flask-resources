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

    def load_request(self, *args, **kwargs):
        """Build response headers."""
        raise NotImplementedError()


class RequestLoader(LoaderMixin):
    """Loaded request representation.

    Loads the content from the request.
    """

    def __init__(self, serializer=None, args_parser=None, *args, **kwargs):
        """Constructor."""
        self.deserializer = deserializer
        self.args_parser = args_parser

    def load_request(self, *args, **kwargs):
        """Build response headers."""
        return self.args_parser.parse(), self.deserializer.deserialize_object()
