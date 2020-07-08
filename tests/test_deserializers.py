# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
# Copyright (C) 2020 Northwestern University.
#
# Flask-Resources is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""Test deserialization."""

import pytest
from flask import Flask

from flask_resources.context import resource_requestctx
from flask_resources.deserializers import JSONDeserializer
from flask_resources.loaders import RequestLoader
from flask_resources.resources import CollectionResource, ResourceConfig


# These classes are in the file because they are under test too
class UniversalDeserializerConfig(ResourceConfig):
    """Resource configuration with deserializer for all endpoints."""

    item_route = "/universal/<id>"
    list_route = "/universal"
    # Because a deserializer is passed directly, it is applied to all endpoints
    request_loaders = {
        # TODO: Rename config and Remove RequestLoader
        "application/json": RequestLoader(deserializer=JSONDeserializer())
    }


class MethodDeserializerConfig(ResourceConfig):
    """Resource configuration with deserializer for a specific endpoint."""

    item_route = "/method/<id>"
    list_route = "/method"
    # Because a deserializer is passed to "search", it is only applied to that endpoint
    request_loaders = {
        # TODO: Rename config and Remove RequestLoader
        "application/json": {"search": RequestLoader(deserializer=JSONDeserializer())}
    }


class DeserializerResource(CollectionResource):
    """Resource implementation to test deserialization."""

    default_config = UniversalDeserializerConfig

    def search(self, *args, **kwargs):
        """Return sent payload."""
        return resource_requestctx.request_content, 200

    def delete(self, *args, **kwargs):
        """Return sent payload."""
        return resource_requestctx.request_content, 200


@pytest.fixture(scope="module")
def app():
    """Application factory fixture."""
    app_ = Flask(__name__)
    custom_bp = DeserializerResource().as_blueprint("universal_resource")
    app_.register_blueprint(custom_bp)
    custom_bp = DeserializerResource(MethodDeserializerConfig).as_blueprint(
        "method_resource"
    )
    app_.register_blueprint(custom_bp)

    return app_


def test_search_endpoint_deserializes_data(client):
    headers = {"content-type": "application/json", "accept": "application/json"}

    response = client.get("/universal", json={"q": "foo=bar"}, headers=headers)

    assert response.status_code == 200
    assert response.json == {"q": "foo=bar"}

    # Works well even if no data
    response = client.get("/universal", headers=headers)

    assert response.status_code == 200
    assert response.json == {}


def test_delete_endpoint_deserializes_data(client):
    headers = {"content-type": "application/json", "accept": "application/json"}

    response = client.delete("/universal/1", json={"tombstone": "baz"}, headers=headers)

    assert response.status_code == 200
    assert response.json == {"tombstone": "baz"}

    # Works well even if no data
    response = client.delete("/universal/1", headers=headers)

    assert response.status_code == 200
    assert response.json == {}


def test_method_deserializer_deserializes_search_only(client):
    headers = {"content-type": "application/json", "accept": "application/json"}

    response = client.get("/method", json={"q": "foo=bar"}, headers=headers)

    assert response.status_code == 200
    assert response.json == {"q": "foo=bar"}

    response = client.delete("/method/1", json={"tombstone": "baz"}, headers=headers)

    assert response.status_code == 415
    assert response.json["status"] == 415
    assert response.json["message"] is not None
