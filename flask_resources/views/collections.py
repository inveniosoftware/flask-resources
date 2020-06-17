# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
#
# Flask-Resources is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""Flask Resources module to create REST APIs."""

from werkzeug.exceptions import HTTPException

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
        _response_handler = self.response_handlers[resource_requestctx.accept_mimetype]
        _response_loader = self.request_loaders[resource_requestctx.payload_mimetype]

        resource_requestctx.request_args = self.create_parser.parse()
        resource_requestctx.data = _response_loader.load_request()

        return _response_handler.make_response(
            *self.resource.create(*args, **kwargs)
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

        try:
            return _response_handler.make_response(*self.resource.read(*args, **kwargs))
        except HTTPException as error:
            # TODO: 1) should this be here, or we use the blueprint error handlers?
            #       records rest have something here.
            #       2) we should check if e.g. a tombstone page is an error or
            #       a normal response.
            return _response_handler.make_error_response(error)

    def put(self, *args, **kwargs):
        """Put."""
        _response_handler = self.response_handlers[resource_requestctx.accept_mimetype]
        # TODO: If application/json is used for both put and post, then they have to
        #       use the same response handler. Possibly this is ok, but need to be
        #       checked. Probably the problems is delegated to partial_update()
        _response_loader = self.request_loaders[resource_requestctx.payload_mimetype]

        try:
            resource_requestctx.data = _response_loader.load_request()
            return _response_handler.make_response(
                *self.resource.update(*args, **kwargs)
            )
        except HTTPException as error:
            return _response_handler.make_error_response(error)

    def patch(self, *args, **kwargs):
        """Patch."""
        _response_handler = self.response_handlers[resource_requestctx.accept_mimetype]
        _response_loader = self.request_loaders[resource_requestctx.payload_mimetype]

        try:
            resource_requestctx.data = _response_loader.load_request()
            return _response_handler.make_response(
                *self.resource.partial_update(*args, **kwargs)
            )
        except HTTPException as error:
            return _response_handler.make_error_response(error)

    def delete(self, *args, **kwargs):
        """Delete."""
        _response_handler = self.response_handlers[resource_requestctx.accept_mimetype]
        # TODO: Delete can potentially have a body - e.g. the tombstone messages.
        #       HTTP spec seems to allow this, but not that common.

        try:
            return _response_handler.make_response(
                *self.resource.delete(*args, **kwargs)
            )
        except HTTPException as error:
            return _response_handler.make_error_response(error)
