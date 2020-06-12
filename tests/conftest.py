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

from flask_resources.resources import CollectionResource


class CustomResource(CollectionResource):
    """Custom resource implementation."""

    def search(self, request_context):
        """Search."""
        pass

    def create(self):
        """Create."""
        pass

    def read(self, id, *args, **kwargs):
        """Read."""
        pass

    def update(self, data, *args, **kwargs):
        """Update."""
        pass

    def partial_update(self, data, *args, **kwargs):
        """Partial update."""
        pass

    def delete(self, *args, **kwargs):
        """Delete."""
        pass


@pytest.fixture(scope="module")
def create_app(instance_path):
    """Application factory fixture."""

    def app(*args, **kwargs):
        """Create app."""
        app_ = Flask(__name__)

        return app_

    return app


@pytest.fixture(scope="module")
def custom_resource_config():
    """Returns a simple custom resource with a custom configuration."""
    return CustomResource()
