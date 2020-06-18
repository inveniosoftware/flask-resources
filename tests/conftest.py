# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
#
# Flask--Resources is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""Pytest configuration.

See https://pytest-invenio.readthedocs.io/ for documentation on which test
fixtures are available.
"""

import pytest
from flask import Flask

from flask_resources.context import resource_requestctx
from flask_resources.resources import CollectionResource, Resource, ResourceConfig


class CustomResourceConfig(ResourceConfig):
    """Custom resource configuration."""

    item_route = "/custom/<id>"
    list_route = "/custom/"


class CustomResource(CollectionResource):
    """Custom resource implementation."""

    def __init__(self, *args, **kwargs):
        """Constructor."""
        super(CustomResource, self).__init__(
            config=CustomResourceConfig, *args, **kwargs
        )
        self.db = {}

    def search(self):
        """Search."""
        query = resource_requestctx.request_args.get("q", "")
        resp = []
        for key, value in self.db.items():
            if query in key or query in value:
                resp.append({"id": key, "content": value})

        return 200, resp

    def create(self):
        """Create."""
        obj = resource_requestctx.request_content
        self.db[obj["id"]] = obj["content"]

        return 201, self.db

    def read(self, id):
        """Read."""
        return 200, {"id": id, "content": self.db[id]}


@pytest.fixture(scope="module")
def app():
    """Application factory fixture."""
    app_ = Flask(__name__)

    default_bp = Resource().as_blueprint("default_resource")
    app_.register_blueprint(default_bp)
    custom_bp = CustomResource().as_blueprint("custom_resource")
    app_.register_blueprint(custom_bp)

    return app_
