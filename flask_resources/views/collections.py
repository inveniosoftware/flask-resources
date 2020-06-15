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
from ..context import resource_requestctx, with_resource_requestctx
from .base import BaseView


class ListView(BaseView):
    """List view representation.

    Allows searching and creating an item in the list.
    """

    def __init__(self, *args, **kwargs):
        """Constructor."""
        super(ListView, self).__init__(*args, **kwargs)
        self.search_parser = self.resource.config.search_request_parser
        self.create_parser = self.resource.config.create_request_parser
        self.response_handler = self.resource.config.list_response_handlers
        self.request_loaders = self.resource.config.item_request_loaders

    @with_resource_requestctx
    def get(self, *args, **kwargs):
        """Search the collection."""
        resource_requestctx.request_args = self.search_parser.parse()
        # FIXME: This selection should come from the request context
        # along with content negotiation (fail fast if not supported)
        _response_handler = self.response_handler["application/json"]

        return _response_handler.make_response(*self.resource.search(*args, **kwargs))

    @with_resource_requestctx
    def post(self, *args, **kwargs):
        """Create an item in the collection."""
        resource_requestctx.request_args = self.create_parser.parse()
        # FIXME: This selection should come from the request context
        # along with content negotiation (fail fast if not supported)
        _response_handler = self.response_handler["application/json"]
        _response_loader = self.request_loaders["application/json"]

        data = _response_loader.load_request()
        return _response_handler.make_response(
            *self.resource.create(data, *args, **kwargs)
        )


class ItemView(BaseView):
    """Item view representation.

    Allows reading, (partial) updating and deleting an item.
    """

    def __init__(self, *args, **kwargs):
        """Constructor."""
        super(ItemView, self).__init__(*args, **kwargs)
        self.item_parser = self.resource.config.item_request_parser
        self.response_handler = self.resource.config.item_response_handlers
        self.request_loaders = self.resource.config.item_request_loaders

    @with_resource_requestctx
    def get(self, *args, **kwargs):
        """Get."""
        # FIXME: This selection should come from the request context
        # along with content negotiation (fail fast if not supported)
        _response_handler = self.response_handler["application/json"]
        _response_loader = self.request_loaders["application/json"]

        return _response_handler.make_response(*self.resource.read(*args, **kwargs))

    @with_resource_requestctx
    def put(self, *args, **kwargs):
        """Put."""
        # FIXME: This selection should come from the request context
        # along with content negotiation (fail fast if not supported)
        _response_handler = self.response_handler["application/json"]
        _response_loader = self.request_loaders["application/json"]

        data = _response_loader.load_request()
        return _response_handler.make_response(
            *self.resource.update(data, *args, **kwargs)
        )

    @with_resource_requestctx
    def patch(self, *args, **kwargs):
        """Patch."""
        # FIXME: This selection should come from the request context
        # along with content negotiation (fail fast if not supported)
        _response_handler = self.response_handler["application/json"]
        _response_loader = self.request_loaders["application/json+patch"]

        data = _response_loader.load_request()
        return _response_handler.make_response(
            *self.resource.partial_update(data, *args, **kwargs)
        )

    @with_resource_requestctx
    def delete(self, *args, **kwargs):
        """Delete."""
        # FIXME: This selection should come from the request context
        # along with content negotiation (fail fast if not supported)
        _response_handler = self.response_handler["application/json"]
        _response_loader = self.request_loaders["application/json"]

        return _response_handler.make_response(*self.resource.delete(*args, **kwargs))
