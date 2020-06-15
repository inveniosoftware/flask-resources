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
from flask_resources.resources import CollectionResource


class CustomResource(CollectionResource):
    """Custom resource implementation."""

    def __init__(self, *args, **kwargs):
        """Constructor."""
        super(CustomResource, self).__init__(*args, **kwargs)
        self.db = {}

    def search(self):
        """Search."""
        query = resource_requestctx.request_args.get("q", "")
        resp = []
        for key, value in self.db.items():
            if query in key or query in value:
                resp.append({"id": key, "content": value})

        return 200, resp

    def create(self, data):
        """Create."""
        self.db[obj["id"]] = obj["content"]

        return 201, self.db

    def read(self, id):
        """Read."""
        return 200, self.db[id]


@pytest.fixture(scope="module")
def create_app(instance_path):
    """Application factory fixture."""

    def app(*args, **kwargs):
        """Create app."""
        app_ = Flask(__name__)

        bp = CustomResource().as_blueprint()
        app_.register_blueprint(bp)

        return app_

    return app
