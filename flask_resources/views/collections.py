# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
# Copyright (C) 2020 Northwestern University.
#
# Flask-Resources is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""Flask Resources module to create REST APIs."""

from flask import request
from werkzeug.exceptions import HTTPException

from ..context import resource_requestctx
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

    @property
    def resource_method(self):
        """Returns string of resource method according to request.method."""
        if request.method == "GET":
            return "search"
        if request.method == "POST":
            return "create"
        return ""

    def get(self, *args, **kwargs):
        """Search the collection."""
        # TODO: Make it so that you don't have to return a tuple. See issue #55
        return self.response_handler.make_list_response(
            *self.resource.search(*args, **kwargs)
        )

    def post(self, *args, **kwargs):
        """Create an item in the collection."""
        return self.response_handler.make_item_response(
            *self.resource.create(*args, **kwargs)  # data is passed in the context
        )

    def put(self, *args, **kwargs):
        """Update the collection."""
        return self.response_handler.make_list_response(
            *self.resource.update_all(*args, **kwargs)
        )

    def delete(self, *args, **kwargs):
        """Delete the collection."""
        return self.response_handler.make_list_response(
            *self.resource.delete_all(*args, **kwargs)
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

    @property
    def resource_method(self):
        """Returns string of resource method according to request.method."""
        if request.method == "GET":
            return "read"
        if request.method == "PUT":
            return "update"
        if request.method == "PATCH":
            return "partial_update"
        if request.method == "DELETE":
            return "delete"
        return ""

    def get(self, *args, **kwargs):
        """Get."""
        return self.response_handler.make_item_response(
            *self.resource.read(*args, **kwargs)
        )

    def put(self, *args, **kwargs):
        """Put."""
        return self.response_handler.make_item_response(
            *self.resource.update(*args, **kwargs)  # data is passed in the context
        )

    def patch(self, *args, **kwargs):
        """Patch."""
        return self.response_handler.make_item_response(
            *self.resource.partial_update(*args, **kwargs)
        )

    def delete(self, *args, **kwargs):
        """Delete."""
        return self.response_handler.make_item_response(
            *self.resource.delete(*args, **kwargs)
        )
