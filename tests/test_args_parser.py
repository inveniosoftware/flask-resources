# -*- coding: utf-8 -*-
#
# Copyright (C) 2020-2021 CERN.
# Copyright (C) 2020-2021 Northwestern University.
#
# Flask-Resources is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""Resources test module."""

import json

import marshmallow as ma
import pytest

from flask_resources import (
    HTTPJSONException,
    Resource,
    ResourceConfig,
    create_error_handler,
    request_parser,
    resource_requestctx,
    route,
)


@pytest.fixture(scope="module")
def resource():
    class TestConfig(ResourceConfig):
        blueprint_name = "test"

    class TestResource(Resource):
        error_handlers = {
            ma.ValidationError: create_error_handler(HTTPJSONException(code=400))
        }

        @request_parser({"id": ma.fields.Int()}, location="args")
        def args(self):
            return resource_requestctx.args, 200

        @request_parser(
            {"id": ma.fields.List(ma.fields.Int())}, location="args", unknown=ma.RAISE
        )
        def multiargs(self):
            return resource_requestctx.args, 200

        @request_parser({"id": ma.fields.Int()}, location="view_args")
        def view_args(self):
            return resource_requestctx.view_args, 200

        @request_parser({"if_match": ma.fields.Int(required=True)}, location="headers")
        def header(self):
            return resource_requestctx.headers, 200

        @request_parser(
            {"if_match": ma.fields.Int(required=True)},
            location="headers",
            unknown=ma.INCLUDE,
        )
        def header_unknown(self):
            return resource_requestctx.headers, 200

        def create_url_rules(self):
            return [
                route("GET", "/args", self.args),
                route("GET", "/multiargs", self.multiargs),
                route("GET", "/viewargs/<id>", self.view_args),
                route("GET", "/header", self.header),
                route("GET", "/header-unknown", self.header_unknown),
            ]

    return TestResource(TestConfig)


def test_args_parsers(client):
    res = client.get("/args?id=1")
    assert res.json == {"id": 1}

    # Invalid value
    res = client.get("/args?id=a")
    assert res.status_code == 400

    # Unknown excluded
    res = client.get("/args?id=1&unknown=1")
    assert res.json == {"id": 1}


def test_multiargs_parsers(client):
    # Test behavior of repeated keys
    res = client.get("/args?id=1&id=2")
    assert res.json == {"id": 1}
    res = client.get("/multiargs?id=1&id=2")
    assert res.json == {"id": [1, 2]}

    # Unknown raises
    res = client.get("/multiargs?id=1&unknown=1")
    assert res.status_code == 400


def test_view_args(client):
    res = client.get("/viewargs/1")
    assert res.json == {"id": 1}
    # Invalid
    res = client.get("/viewargs/a")
    assert res.status_code == 400


def test_headers(client):
    # Test headers
    res = client.get("/header", headers={"if-match": "1"})
    assert res.json == {"if_match": 1}
    # header required
    res = client.get("/header")
    assert res.status_code == 400

    # include unknowns
    res = client.get("/header-unknown", headers={"if-match": "1"})
    assert res.json["if_match"] == 1
    assert "user_agent" in res.json
