# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
# Copyright (C) 2020 Northwestern University.
#
# Flask-Resources is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""Parses test module."""

import pytest
from flask import Flask

from flask_resources.context import resource_requestctx
from flask_resources.resources import CollectionResource, ResourceConfig

# NOTE: mimetype headers have to be provided in general, but the args parsing is not
#       dependent on them specifically directly i.e. it could have been xml if xml
#       were implemented
HEADERS = {"content-type": "application/json", "accept": "application/json"}


# These classes are in the file because they are under test too
class HeaderParserConfig(ResourceConfig):
    """Resource configuration for headers test (nothing special for now)."""

    item_route = "/headers/<id>"
    list_route = "/headers"


class HeadersResource(CollectionResource):
    """Resource implementation to test headers."""

    default_config = HeaderParserConfig

    def _headers_to_dict(self):
        return dict(resource_requestctx.headers.items())

    def search(self, *args, **kwargs):
        """Perform a search over the items."""
        return self._headers_to_dict(), 200

    def create(self, *args, **kwargs):
        """Create an item."""
        return self._headers_to_dict(), 200

    def read(self, *args, **kwargs):
        """Read an item."""
        # import pdb; pdb.set_trace()
        return self._headers_to_dict(), 200

    def update(self, *args, **kwargs):
        """Update an item."""
        return self._headers_to_dict(), 200

    def partial_update(self, *args, **kwargs):
        """Partial update an item."""
        return self._headers_to_dict(), 200

    def delete(self, *args, **kwargs):
        """Delete an item."""
        return self._headers_to_dict(), 200


@pytest.fixture(scope="module")
def app():
    """Application factory fixture."""
    app_ = Flask(__name__)
    custom_bp = HeadersResource().as_blueprint("headers_resource")
    app_.register_blueprint(custom_bp)
    return app_


@pytest.fixture(scope="module")
def expected_headers():
    return {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Host": "localhost",
        "User-Agent": "werkzeug/1.0.1",
    }


def test_headers_read_endpoint(client, expected_headers):
    response = client.get("/headers/1", headers=HEADERS)
    assert response.status_code == 200
    assert expected_headers == response.json


def test_headers_search_endpoint(client, expected_headers):
    response = client.get("/headers", headers=HEADERS)
    assert response.status_code == 200
    assert expected_headers == response.json


def test_headers_create_endpoint(client, expected_headers):
    response = client.post("/headers", headers=HEADERS)
    assert response.status_code == 200
    assert expected_headers == response.json


def test_headers_update_endpoint(client, expected_headers):
    response = client.put("/headers/1", headers=HEADERS)
    assert response.status_code == 200
    assert expected_headers == response.json


def test_headers_partial_update_endpoint(client, expected_headers):
    response = client.patch("/headers/1", headers=HEADERS)
    assert response.status_code == 200
    assert expected_headers == response.json


def test_headers_delete_endpoint(client, expected_headers):
    response = client.delete("/headers/1", headers=HEADERS)
    assert response.status_code == 200
    assert expected_headers == response.json
