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


class CustomSerializer(SerializerMixin):
    """Custom serializer implementation."""

    def serialize_object(self, object, response_ctx, *args, **kwargs):
        """Custom object serialization."""
        pass

    def serialize_object_list(self, object_list, response_ctx, *args, **kwargs):
        """Custom object list serialization."""
        pass


class CustomResourceConfig:
    """Custom resource configuration."""

    item_handlers = {"application/json": ItemResponse(CustomSerializer)}


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
    return CustomResource(config=CustomResourceConfig)
