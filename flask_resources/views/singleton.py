# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
#
# Flask-Resources is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""Flask Resources module to create REST APIs."""

from flask import request

from .base import BaseView


class SingletonView(BaseView):
    """Parse request args and create a request context.

    Note that the resource route should contain the `<id>` param.
    """

    def __init__(self, *args, **kwargs):
        """Constructor."""
        super(SingletonView, self).__init__(*args, **kwargs)
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
        if request.method == "POST":
            return "create"
        return ""

    def post(self, *args, **kwargs):
        """Post."""
        return self.response_handler.make_item_response(
            *self.resource.create(*args, **kwargs)  # data is passed in the context
        )

    def get(self, *args, **kwargs):
        """Get."""
        return self.response_handler.make_item_response(
            *self.resource.read(*args, **kwargs)  # data is passed in the context
        )

    def put(self, *args, **kwargs):
        """Put."""
        return self.response_handler.make_item_response(
            *self.resource.update(*args, **kwargs)  # data is passed in the context
        )

    def patch(self, *args, **kwargs):
        """Patch."""
        return self.response_handler.make_item_response(
            *self.resource.partial_update(
                *args, **kwargs
            )  # data is passed in the context
        )

    def delete(self, *args, **kwargs):
        """Delete."""
        return self.response_handler.make_item_response(
            *self.resource.delete(*args, **kwargs)  # data is passed in the context
        )
