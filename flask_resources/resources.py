# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
# Copyright (C) 2020 Northwestern University.
#
# Flask-Resources is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Resource view."""

from flask import Blueprint
from marshmallow import ValidationError

from .deserializers import JSONDeserializer
from .errors import create_errormap_handler
from .loaders import RequestLoader
from .parsers import ArgsParser
from .responses import Response
from .serializers import JSONSerializer
from .views import ItemView, ListView, SingletonView

ITEM_VIEW_SUFFIX = "_item"
LIST_VIEW_SUFFIX = "_list"


class ResourceConfig:
    """Base resource configuration."""

    request_loaders = {
        "application/json": RequestLoader(deserializer=JSONDeserializer())
    }
    response_handlers = {"application/json": Response(JSONSerializer())}
    item_route = "/resources/<id>"
    list_route = "/resources/"
    request_url_args_parser = ArgsParser()
    default_content_type = "application/json"
    default_accept_mimetype = "application/json"


class Resource:
    """Resource controller interface."""

    default_config = ResourceConfig

    def __init__(self, config=None):
        """Initialize the base resource."""
        # TODO: The config should be checked to see that it is consistent. See issue #57
        self.config = config or self.default_config
        self.bp_name = None

    # Primary interface
    def search(self):
        """Perform a search over the items."""
        return [], 200

    def create(self):
        """Create an item."""
        return {}, 200

    def read(self):
        """Read an item."""
        return {}, 200

    def update(self):
        """Update an item."""
        return {}, 200

    def partial_update(self):
        """Partial update an item."""
        return {}, 200

    def delete(self):
        """Delete an item."""
        return {}, 200

    # Secondary interface
    def as_blueprint(self, name, **bp_kwargs):
        """Create blueprint and register rules only for the RecordResource."""
        self.bp_name = name
        blueprint = Blueprint(name, __name__, **bp_kwargs)

        for rule in self.create_url_rules(name):
            blueprint.add_url_rule(**rule)

        for exc_or_code, error_handler in self.create_errormap_handlers():
            blueprint.register_error_handler(exc_or_code, error_handler)

        return blueprint

    def create_url_rules(self, bp_name):
        """Create url rules."""
        return [
            {
                "rule": self.config.item_route,
                "view_func": ItemView.as_view(
                    name=f"{bp_name}",
                    resource=self,
                ),
            }
        ]

    def create_errormap_handlers(self):
        """Create error handlers."""
        error_map = getattr(self.config, "error_map", {})
        return error_map.items()


class CollectionResource(Resource):
    """CollectionResource."""

    def update_all(self):
        """Delete an item."""
        return [], 200

    def delete_all(self):
        """Delete an item."""
        return [], 200

    def create_url_rules(self, bp_name):
        """Create url rules."""
        return [
            {
                "rule": self.config.item_route,
                "view_func": ItemView.as_view(
                    name=f"{bp_name}{ITEM_VIEW_SUFFIX}",
                    resource=self,
                ),
            },
            {
                "rule": self.config.list_route,
                "view_func": ListView.as_view(
                    name=f"{bp_name}{LIST_VIEW_SUFFIX}",
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
                    name=f"{bp_name}",
                    resource=self,
                ),
            }
        ]
