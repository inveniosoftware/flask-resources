# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
#
# Flask-Resources is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Library for easily implementing REST APIs."""

from flask import Blueprint, abort

from .views import ItemView, ListView, SingletonView

ITEM_VIEW_SUFFIX = "_item_view"
LIST_VIEW_SUFFIX = "_list_view"
SINGLETON_VIEW_SUFFIX = "_singleton_view"


class Resource(object):
    """Resource controller interface."""

    def __init__(self, controller, config):
        """Initialize the base resource."""
        self.controller = controller
        self.config = config
        self.bp_name = None

    # Primary interface
    def search(self, request_context):
        """Perform a search over the items."""
        # TODO: the resource itself shouldn't be "request"-aware. Returning of
        # HTTP responses should be done in views. Maybe some base
        # error/exception classes can be defined to help?
        abort(405)

    def create(self):
        """Create an item."""
        abort(405)

    def read(self, *args, **kwargs):
        """Read an item."""
        abort(405)

    def update(self, data, *args, **kwargs):
        """Update an item."""
        abort(405)

    def partial_update(self, data, *args, **kwargs):
        """Partial update an item."""
        abort(405)

    def delete(self, *args, **kwargs):
        """Delete an item."""
        abort(405)

    # Secondary interface
    def as_blueprint(self, name, **bp_kwargs):
        """Create blueprint and register rules only for the RecordResource."""
        self.bp_name = name
        blueprint = Blueprint(name, __name__, **bp_kwargs)

        for rule in self.create_url_rules(name):
            blueprint.add_url_rule(**rule)

        return blueprint

    def create_url_rules(self, bp_name):
        """Create url rules."""
        return [
            {
                "rule": self.config.item_route,
                "view_func": ItemView.as_view(
                    name="{}{}".format(bp_name, ITEM_VIEW_SUFFIX),
                    resource=self,
                ),
            }
        ]

    def create_error_handlers(self):
        """Create error handlers."""
        return []

    def load_item_from_request(self):
        """Load item from request."""
        # FIXME: Code default
        # self.config.item_loader()
        pass

    def make_list_response(self, item_list, http_code):
        """Make list response."""
        # FIXME: Code default
        # self.config.list_serializer()
        pass

    def make_item_response(self, item, http_code):
        """Make item response."""
        # FIXME: Code default
        # self.config.item_serializer()
        pass

    def make_error_response(self, error_data, http_code):
        """Make error response."""
        # FIXME: Code default
        # self.config.error_serializer()
        pass


class CollectionResource(Resource):
    """CollectionResource."""

    def create_url_rules(self, bp_name):
        """Create url rules."""
        return [
            {
                "rule": self.config.item_route,
                "view_func": ItemView.as_view(
                    name="{}{}".format(bp_name, ITEM_VIEW_SUFFIX),
                    resource=self,
                ),
            },
            {
                "rule": self.config.list_route,
                "view_func": ListView.as_view(
                    name="{}{}".format(bp_name, LIST_VIEW_SUFFIX),
                    resource=self,
                ),
            },
        ]


class SingletonResource(Resource):
    """SingletonResource."""

    def create_url_rules(self, bp_name):
        """Create url rules."""
        return [
            {
                "rule": self.config.list_route,
                "view_func": SingletonView.as_view(
                    name="{}{}".format(bp_name, SINGLETON_VIEW_SUFFIX),
                    resource=self,
                ),
            }
        ]
