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
from webargs import fields
from werkzeug.exceptions import HTTPException

from flask_resources.context import resource_requestctx
from flask_resources.errors import (
    HTTPJSONException,
    create_errormap_handler,
    handle_http_exception,
)
from flask_resources.parsers import ArgsParser
from flask_resources.resources import CollectionResource, ResourceConfig

# NOTE: mimetype headers have to be provided in general, but the args parsing is not
#       dependent on them specifically directly i.e. it could have been xml if xml
#       were implemented
HEADERS = {"content-type": "application/json", "accept": "application/json"}


# These classes are in the file because they are under test too
class UniversalParserConfig(ResourceConfig):
    """Resource configuration with ArgsParser for all endpoints."""

    item_route = "/universal/<id>"
    list_route = "/universal"
    # Because an ArgsParser is passed directly, it is applied to all endpoints
    request_url_args_parser = ArgsParser(
        {"num": fields.Int(), "lang": fields.String(missing="")}, allow_unknown=False
    )


class MethodParserConfig(ResourceConfig):
    """Resource configuration with ArgsParser for a specific endpoint."""

    item_route = "/method/<id>"
    list_route = "/method"
    # Because an ArgsParser is passed to "search", it is only applied to that endpoint
    request_url_args_parser = {
        "search": ArgsParser({"num": fields.Int(), "lang": fields.String(missing="")})
    }


class ParserResource(CollectionResource):
    """Resource implementation to test parsers."""

    default_config = UniversalParserConfig

    def search(self, *args, **kwargs):
        """Perform a search over the items."""
        return resource_requestctx.request_args, 200

    def create(self, *args, **kwargs):
        """Create an item."""
        return resource_requestctx.request_args, 200

    def read(self, *args, **kwargs):
        """Read an item."""
        return resource_requestctx.request_args, 200

    def update(self, *args, **kwargs):
        """Update an item."""
        return resource_requestctx.request_args, 200

    def partial_update(self, *args, **kwargs):
        """Partial update an item."""
        return resource_requestctx.request_args, 200

    def delete(self, *args, **kwargs):
        """Delete an item."""
        return resource_requestctx.request_args, 200


@pytest.fixture(scope="module")
def app():
    """Application factory fixture."""
    app_ = Flask(__name__)
    custom_bp = ParserResource().as_blueprint("universal_resource")
    app_.register_blueprint(custom_bp)
    custom_bp = ParserResource(MethodParserConfig).as_blueprint("method_resource")
    app_.register_blueprint(custom_bp)
    app_.register_error_handler(HTTPException, handle_http_exception)
    return app_


def test_universal_parser_parses_one_endpoint(client):
    response = client.get("/universal/1?num=10", headers=HEADERS)

    assert response.status_code == 200
    assert response.json["num"] == 10
    assert response.json["lang"] == ""


def test_universal_parser_parses_all_endpoints(client):
    # search
    response = client.get("/universal?num=10", headers=HEADERS)
    assert response.status_code == 200
    assert response.json["num"] == 10
    assert response.json["lang"] == ""

    # create
    response = client.post("/universal?num=10", headers=HEADERS)
    assert response.status_code == 200
    assert response.json["num"] == 10
    assert response.json["lang"] == ""

    # read -- covered above

    # update
    response = client.put("/universal/1?num=10", headers=HEADERS)
    assert response.status_code == 200
    assert response.json["num"] == 10
    assert response.json["lang"] == ""

    # partial update
    response = client.patch("/universal/1?num=10", headers=HEADERS)
    assert response.status_code == 200
    assert response.json["num"] == 10
    assert response.json["lang"] == ""

    # delete
    response = client.delete("/universal/1?num=10", headers=HEADERS)
    assert response.status_code == 200
    assert response.json["num"] == 10
    assert response.json["lang"] == ""


def test_method_parser_parses_only_method_endpoint(client):
    # search
    response = client.get("/method?num=10", headers=HEADERS)
    assert response.status_code == 200
    assert response.json["num"] == 10
    assert response.json["lang"] == ""

    # Other methods should return an empty json
    # Passing query strings when no parser for them is totally fine
    # they are just not extracted.

    # create
    response = client.post("/method?num=10", headers=HEADERS)
    assert response.status_code == 200
    assert response.json == {}

    # read
    response = client.put("/method/1?num=10", headers=HEADERS)
    assert response.status_code == 200
    assert response.json == {}

    # update
    response = client.put("/method/1?num=10", headers=HEADERS)
    assert response.status_code == 200
    assert response.json == {}

    # partial update
    response = client.patch("/method/1?num=10", headers=HEADERS)
    assert response.status_code == 200
    assert response.json == {}

    # delete
    response = client.delete("/method/1?num=10", headers=HEADERS)
    assert response.status_code == 200
    assert response.json == {}


def test_parser_raises_400(client):
    response = client.get("/method?num=NotANumber", headers=HEADERS)

    assert response.status_code == 400
    assert response.json["status"] == 400
    assert response.json["message"] is not None


def test_parser_includes_or_excludes_unknown_args(client):
    response = client.get("/method?num=10&foo=20&bar=1&foo=10", headers=HEADERS)
    assert response.status_code == 200
    assert response.json == {"num": 10, "lang": "", "foo": ["20", "10"], "bar": ["1"]}

    response = client.get("/universal?num=10&foo=20&bar=1&foo=10", headers=HEADERS)
    assert response.status_code == 200
    assert response.json == {"num": 10, "lang": ""}
