# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
#
# Flask-Resources is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""Flask Resources module to create REST APIs."""

from werkzeug.exceptions import HTTPException

from ..context import resource_requestctx
from ..parsers import create_request_parser, item_request_parser, search_request_parser
from .base import BaseView


class ListView(BaseView):
    """List view representation.

    Allows searching and creating an item in the list.
    """

    def __init__(self, *args, **kwargs):
        """Constructor."""
        super(ListView, self).__init__(*args, **kwargs)
        self.response_handlers = self.resource.config.list_response_handlers
        self.request_loaders = self.resource.config.request_loaders

    def get(self, *args, **kwargs):
        """Search the collection."""
        _response_handler = self.response_handlers[resource_requestctx.accept_mimetype]
        _request_loader = self.request_loaders[resource_requestctx.payload_mimetype]

        resource_requestctx.request_args = _request_loader.load_search_request()

        return _response_handler.make_response(*self.resource.search(*args, **kwargs))

    def post(self, *args, **kwargs):
        """Create an item in the collection."""
        _response_handler = self.response_handlers[resource_requestctx.accept_mimetype]
        _request_loader = self.request_loaders[resource_requestctx.payload_mimetype]

        resource_requestctx.request_args, data = _request_loader.load_create_request()

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
        self.response_handlers = self.resource.config.item_response_handlers
        self.request_loaders = self.resource.config.request_loaders

    def get(self, *args, **kwargs):
        """Get."""
        _response_handler = self.response_handlers[resource_requestctx.accept_mimetype]
        _request_loader = self.request_loaders[resource_requestctx.payload_mimetype]

        try:
            (
                resource_requestctx.request_args,  # Will give the id
                data,  # Will be empty
            ) = _request_loader.load_item_request()

            return _response_handler.make_response(*self.resource.read(*args, **kwargs))
        except HTTPException as error:
            return _response_handler.make_error_response(error)

    def put(self, *args, **kwargs):
        """Put."""
        _response_handler = self.response_handlers[resource_requestctx.accept_mimetype]
        _request_loader = self.request_loaders[resource_requestctx.payload_mimetype]

        try:
            (
                resource_requestctx.request_args,  # Will give the id
                data,
            ) = _request_loader.load_item_request()

            return _response_handler.make_response(
                *self.resource.update(data, *args, **kwargs)
            )
        except HTTPException as error:
            return _response_handler.make_error_response(error)

    def patch(self, *args, **kwargs):
        """Patch."""
        _response_handler = self.response_handlers[resource_requestctx.accept_mimetype]
        _request_loader = self.request_loaders[resource_requestctx.payload_mimetype]

        try:
            (
                resource_requestctx.request_args,  # Will give the id
                data,
            ) = _request_loader.load_item_request()

            return _response_handler.make_response(
                *self.resource.partial_update(data, *args, **kwargs)
            )
        except HTTPException as error:
            return _response_handler.make_error_response(error)

    def delete(self, *args, **kwargs):
        """Delete."""
        _response_handler = self.response_handlers[resource_requestctx.accept_mimetype]
        _request_loader = self.request_loaders[resource_requestctx.payload_mimetype]

        try:
            (
                resource_requestctx.request_args,  # Will give the id
                data,  # Will be empty
            ) = _request_loader.load_item_request()

            return _response_handler.make_response(
                *self.resource.delete(*args, **kwargs)
            )
        except HTTPException as error:
            return _response_handler.make_error_response(error)
