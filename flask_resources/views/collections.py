# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
#
# Flask-Resources is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""Flask Resources module to create REST APIs."""

from werkzeug.exceptions import HTTPException

from ..context import resource_requestctx
from ..parsers import search_request_parser
from .base import BaseView


class ListView(BaseView):
    """List view representation.

    Allows searching and creating an item in the list.
    """

    def __init__(self, *args, **kwargs):
        """Constructor."""
        super(ListView, self).__init__(*args, **kwargs)
        # is defined by response_handler decorator
        self.response_handler = None
        # is defined by response_loader decorator
        self.request_loader = None

    def get(self, *args, **kwargs):
        """Search the collection."""
        resource_requestctx.update(self.request_loader.load_search_request())

        return self.response_handler.make_list_response(
            *self.resource.search(*args, **kwargs)
        )

    def post(self, *args, **kwargs):
        """Create an item in the collection."""
        resource_requestctx.update(self.request_loader.load_item_request())

        return self.response_handler.make_item_response(
            *self.resource.create(*args, **kwargs)  # data is passed in the context
        )


class ItemView(BaseView):
    """Item view representation.

    Allows reading, (partial) updating and deleting an item.
    """

    def __init__(self, *args, **kwargs):
        """Constructor."""
        super(ItemView, self).__init__(*args, **kwargs)
        # is defined by response_handler decorator
        self.response_handler = None
        # is defined by response_loader decorator
        self.request_loader = None

    def get(self, *args, **kwargs):
        """Get."""
        try:
            return self.response_handler.make_item_response(
                *self.resource.read(*args, **kwargs)
            )
        except HTTPException as error:
            return self.response_handler.make_error_response(error)

    def put(self, *args, **kwargs):
        """Put."""
        try:
            resource_requestctx.update(self.request_loader.load_item_request())
            return self.response_handler.make_item_response(
                *self.resource.update(*args, **kwargs)  # data is passed in the context
            )
        except HTTPException as error:
            return self.response_handler.make_error_response(error)

    def patch(self, *args, **kwargs):
        """Patch."""
        try:
            resource_requestctx.update(self.request_loader.load_item_request())
            return self.response_handler.make_item_response(
                *self.resource.partial_update(*args, **kwargs)
            )
        except HTTPException as error:
            return self.response_handler.make_error_response(error)

    def delete(self, *args, **kwargs):
        """Delete."""
        try:
            return self.response_handler.make_item_response(
                *self.resource.delete(*args, **kwargs)
            )
        except HTTPException as error:
            return self.response_handler.make_error_response(error)
