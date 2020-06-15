# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
#
# Flask-Resources is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Resource view."""

from flask import Blueprint

from .loaders import JSONLoader, JSONPatchLoader
from .response import ItemResponse, ListResponse
from .serializers import JSONSerializer
from .views import ItemView, ListView, SingletonView

ITEM_VIEW_SUFFIX = "_item_view"
LIST_VIEW_SUFFIX = "_list_view"
SINGLETON_VIEW_SUFFIX = "_singleton_view"


class ResourceConfig:
    """Base resource configuration."""

    item_request_loaders = {
        "application/json": JSONLoader(),
        "application/json+patch": JSONPatchLoader(),
    }
    item_response_handlers = {"application/json": ItemResponse(JSONSerializer)}
    item_route = "resources/<id>"
    list_response_handlers = {"application/json": ListResponse(JSONSerializer)}
    list_route = "resources/"


class Resource:
    """Resource controller interface."""

    def __init__(self, config=ResourceConfig, *args, **kwargs):
        """Initialize the base resource."""
        self.config = config
        self.bp_name = None

    # Primary interface
    def search(self, request_context):
        """Perform a search over the items."""
        return 405

    def create(self):
        """Create an item."""
        return 405

    def read(self, *args, **kwargs):
        """Read an item."""
        return 405

    def update(self, data, *args, **kwargs):
        """Update an item."""
        return 405

    def partial_update(self, data, *args, **kwargs):
        """Partial update an item."""
        return 405

    def delete(self, *args, **kwargs):
        """Delete an item."""
        return 405

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
                    name="{}{}".format(bp_name, ITEM_VIEW_SUFFIX), resource=self,
                ),
            }
        ]

    def create_error_handlers(self):
        """Create error handlers."""
        return []


class CollectionResource(Resource):
    """CollectionResource."""

    def create_url_rules(self, bp_name):
        """Create url rules."""
        return [
            {
                "rule": self.config.item_route,
                "view_func": ItemView.as_view(
                    name="{}{}".format(bp_name, ITEM_VIEW_SUFFIX), resource=self,
                ),
            },
            {
                "rule": self.config.list_route,
                "view_func": ListView.as_view(
                    name="{}{}".format(bp_name, LIST_VIEW_SUFFIX), resource=self,
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
                    name="{}{}".format(bp_name, SINGLETON_VIEW_SUFFIX), resource=self,
                ),
            }
        ]
