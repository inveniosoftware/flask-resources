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
from ..content_negotiation import content_negotiation
from ..context import resource_requestctx
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
        self.response_handlers = self.resource.config.list_response_handlers
        self.request_loaders = self.resource.config.item_request_loaders

    def get(self, *args, **kwargs):
        """Search the collection."""
        resource_requestctx.request_args = self.search_parser.parse()
        _response_handler = self.response_handlers[resource_requestctx.accept_mimetype]

        return _response_handler.make_response(*self.resource.search(*args, **kwargs))

    def post(self, *args, **kwargs):
        """Create an item in the collection."""
        resource_requestctx.request_args = self.create_parser.parse()
        _response_handler = self.response_handlers[resource_requestctx.accept_mimetype]
        _response_loader = self.request_loaders[resource_requestctx.payload_mimetype]

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
        self.response_handlers = self.resource.config.item_response_handlers
        self.request_loaders = self.resource.config.item_request_loaders

    def get(self, *args, **kwargs):
        """Get."""
        _response_handler = self.response_handlers[resource_requestctx.accept_mimetype]

        return _response_handler.make_response(*self.resource.read(*args, **kwargs))

    def put(self, *args, **kwargs):
        """Put."""
        _response_handler = self.response_handlers[resource_requestctx.accept_mimetype]
        _response_loader = self.request_loaders[resource_requestctx.payload_mimetype]

        data = _response_loader.load_request()
        return _response_handler.make_response(
            *self.resource.update(data, *args, **kwargs)
        )

    def patch(self, *args, **kwargs):
        """Patch."""
        _response_handler = self.response_handlers[resource_requestctx.accept_mimetype]
        _response_loader = self.request_loaders[resource_requestctx.payload_mimetype]

        data = _response_loader.load_request()
        return _response_handler.make_response(
            *self.resource.partial_update(data, *args, **kwargs)
        )

    def delete(self, *args, **kwargs):
        """Delete."""
        _response_handler = self.response_handlers[resource_requestctx.accept_mimetype]

        return _response_handler.make_response(*self.resource.delete(*args, **kwargs))
