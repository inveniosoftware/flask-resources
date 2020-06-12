# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
#
# Flask-Resources is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""Flask Resources module to create REST APIs."""

from ..args.parsers import (
    create_request_parser,
    item_request_parser,
    search_request_parser,
)
from ..context import resource_requestctx
from .base import BaseView


class ListView(BaseView):
    """List view representation.

    Allows searching and creating an item in the list.
    """

    def __init__(self, *args, **kwargs):
        """Constructor."""
        super(ListView, self).__init__(*args, **kwargs)
        # FIXME: Parsers here? It is a naming dependency on the resource
        # config.
        # However there is no default config in flask-resources
        self.search_parser = self.resource.config.search_request_parser
        self.create_parser = self.resource.config.create_request_parser
        self.response_handler = self.resource.config.list_response_handler

    def get(self, *args, **kwargs):
        """Search the collection."""
        resource_requestctx.request_args = self.search_parser.parse()

        self.response_handler.make_response(self.resource.search())

    def post(self, *args, **kwargs):
        """Create an item in the collection."""
        resource_requestctx.request_args = self.create_parser.parse()

        self.response_handler.make_response(self.resource.create())


class ItemView(BaseView):
    """Item view representation.

    Allows reading, (partial) updating and deleting an item.
    """

    def __init__(self, *args, **kwargs):
        """Constructor."""
        super(ItemView, self).__init__(*args, **kwargs)
        self.item_parser = self.resource.config.item_request_parser
        self.response_handler = self.resource.config.item_response_handler

    def get(self, *args, **kwargs):
        """Get."""
        self.response_handler.make_response(self.resource.read())

    def put(self, *args, **kwargs):
        """Put."""
        self.response_handler.make_response(self.resource.update())

    def patch(self, *args, **kwargs):
        """Patch."""
        self.response_handler.make_response(self.resource.partial_update())

    def delete(self, *args, **kwargs):
        """Delete."""
        self.response_handler.make_response(self.resource.delete())
