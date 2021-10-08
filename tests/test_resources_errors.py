# -*- coding: utf-8 -*-
#
# Copyright (C) 2020-2021 CERN.
# Copyright (C) 2020-2021 Northwestern University.
#
# Flask-Resources is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""Resources test module."""

import json

import pytest
from flask import Flask, abort
from werkzeug.exceptions import HTTPException

from flask_resources import Resource, ResourceConfig, create_error_handler, route
from flask_resources.errors import HTTPJSONException


@pytest.fixture(scope="module")
def resource():
    class Config(ResourceConfig):
        blueprint_name = "hello_world"
        error_handlers = {
            403: create_error_handler(
                HTTPJSONException(code=403, description="Overwrite existing")
            ),
        }

    class HelloWorldResource(Resource):
        error_handlers = {
            RuntimeError: create_error_handler(
                HTTPJSONException(code=400, description="Bad request")
            ),
            403: create_error_handler(
                HTTPJSONException(code=405, description="Permission defined")
            ),
        }

        def runtime(self):
            raise RuntimeError()

        def abort403(self):
            # Used for testing overriding
            abort(403)

        def abort404(self):
            # A standard HTTPException
            abort(404)

        def unhandled(self):
            raise Exception("Boom")

        def create_url_rules(self):
            return [
                route("GET", "/runtime", self.runtime),
                route("GET", "/abort403", self.abort403),
                route("GET", "/abort404", self.abort404),
                route("GET", "/unhandled", self.unhandled),
            ]

    return HelloWorldResource(Config())


def test_error_handlers(client):
    # Test that the error was handled, and that the response is JSON
    res = client.get("/runtime")
    assert res.status_code == 400
    assert res.json["status"] == 400

    res = client.get("/abort403")
    assert res.status_code == 403
    assert res.json["status"] == 403

    res = client.get("/abort404")
    assert res.status_code == 404
    assert res.json["status"] == 404

    res = client.get("/unhandled")
    assert res.status_code == 500
    assert res.json["status"] == 500
