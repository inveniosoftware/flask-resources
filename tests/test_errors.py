# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
#
# Flask--Resources is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""Errors test module."""

import pytest
from flask import Flask

from flask_resources.resources import CollectionResource, Resource, ResourceConfig


# These classes are in the file because they are under test too
class CustomConfig(ResourceConfig):
    """Custom resource configuration."""

    item_route = "/custom/<id>"
    list_route = "/custom/"


class CustomResource(CollectionResource):
    """Custom resource implementation."""

    default_config = CustomConfig


@pytest.fixture(scope="module")
def app():
    """Application factory fixture."""
    app_ = Flask(__name__)
    custom_bp = CustomResource().as_blueprint("custom_resource")
    app_.register_blueprint(custom_bp)
    return app_


def test_404_if_no_route(client):
    response = client.get("/foo")
    assert response.status_code == 404

    response = client.post("/foo")
    assert response.status_code == 404

    response = client.put("/foo")
    assert response.status_code == 404

    response = client.patch("/foo")
    assert response.status_code == 404

    response = client.delete("/foo")
    assert response.status_code == 404


def test_405_if_route_but_no_method(client):
    # TODO: Only implement MethodView methods for defined Resource methods. Only then
    #       can we test that all methods return 405 (and not just the ones this library
    #       didn't define in its MethodViews
    # NOTE: For now we just test the methods that this library
    #       didn't define in its MethodViews
    # List-level
    response = client.put("/custom/")
    assert response.status_code == 405

    response = client.delete("/custom/")
    assert response.status_code == 405

    # Item-level
    response = client.post("/custom/1")
    assert response.status_code == 405


def test_406_if_route_method_but_unsupported_accept(client):
    # NOTE: By default we don't accept any mimetype at all
    headers = {"accept": "application/marcxml+garbage"}

    # List-level
    response = client.get("/custom/", headers=headers)
    assert response.status_code == 406

    response = client.post("/custom/", headers=headers)
    assert response.status_code == 406

    # Item-level
    response = client.get("/custom/1", headers=headers)
    assert response.status_code == 406

    response = client.put("/custom/1", headers=headers)
    assert response.status_code == 406

    response = client.patch("/custom/1", headers=headers)
    assert response.status_code == 406

    response = client.delete("/custom/1", headers=headers)
    assert response.status_code == 406


def test_415_if_route_method_accept_but_unsupported_content_type(client):
    # NOTE: Right now, we rely entirely on headers for payload assessment.
    headers = {"accept": "application/json", "content-type": "application/json+garbage"}

    # NOTE: We only test methods that accept a payload
    # List-level
    response = client.post("/custom/", headers=headers)
    assert response.status_code == 415

    # Item-level
    response = client.put("/custom/1", headers=headers)
    assert response.status_code == 415

    response = client.patch("/custom/1", headers=headers)
    assert response.status_code == 415
