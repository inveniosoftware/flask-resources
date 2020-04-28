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
from .base import BaseView, with_resource_requestctx


class ListView(BaseView):
    """List view representation.

    Allows searching and creating an item in the list."""

    def __init__(self, resource=None, *args, **kwargs):
        super(ListView, self).__init__(resource=resource, *args, **kwargs)
        # FIXME: Parsers here? It is a naming dependency on the resource config.
        # However there is no default config in flask-resources
        self.search_parser = resource.config.search_request_parser
        self.create_parser = resource.config.create_request_parser

    @with_resource_requestctx
    def get(self, *args, **kwargs):
        """Search the collection."""
        resource_requestctx.request_args = self.search_parser.parse()
        return self.resource.search()

    @with_resource_requestctx
    def post(self, *args, **kwargs):
        """Create an item in the collection."""
        resource_requestctx.request_args = self.create_parser.parse()
        return self.resource.create()


class ItemView(BaseView):
    """Item view representation.
    
    Allows reading, (partial) updating and deleting an item."""

    def __init__(self, resource=None, *args, **kwargs):
        super(ItemView, self).__init__(resource=resource, *args, **kwargs)
        self.item_parser = resource.config.item_request_parser

    @with_resource_requestctx
    def get(self, *args, **kwargs):
        return self.resource.read()

    @with_resource_requestctx
    def put(self, *args, **kwargs):
        return self.resource.update()

    @with_resource_requestctx
    def patch(self, *args, **kwargs):
        return self.resource.partial_update()

    @with_resource_requestctx
    def delete(self, *args, **kwargs):
        return self.resource.delete()
