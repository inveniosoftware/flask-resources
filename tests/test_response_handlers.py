# -*- coding: utf-8 -*-
#
# Copyright (C) 2020-2021 CERN.
# Copyright (C) 2020-2021 Northwestern University.
#
# Flask-Resources is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""Resources test module."""

import marshmallow as ma
import pytest
from flask import Flask

from flask_resources import (
    Resource,
    ResourceConfig,
    ResponseHandler,
    response_handler,
    route,
)
from flask_resources.serializers.json import MarshmallowJSONSerializer


@pytest.fixture(scope="module")
def resource():
    class TestSchema(ma.Schema):
        id = ma.fields.String()

    def my_headers(obj_or_list, code, many=False):
        return {"etag": "test", "content-type": "application/json"}

    class TestConfig(ResourceConfig):
        blueprint_name = "test"

        response_handlers = {
            "application/json": ResponseHandler(
                MarshmallowJSONSerializer(TestSchema), headers=my_headers
            ),
            "application/vnd.test+json": ResponseHandler(
                MarshmallowJSONSerializer(TestSchema),
            ),
        }

    class TestResource(Resource):
        @response_handler()
        def one(self):
            return {"id": "one"}, 200

        @response_handler(many=True)
        def many(self):
            return [{"id": "many"}], 201

        def create_url_rules(self):
            return [
                route("GET", "/one", self.one),
                route("GET", "/many", self.many),
            ]

    return TestResource(TestConfig)


def test_one(client):
    res = client.get("/one", headers={"accept": "application/json"})
    assert res.headers["ETag"] == "test"
    assert res.json == {"id": "one"}

    res = client.get("/one", headers={"accept": "application/vnd.test+json"})
    assert "ETag" not in res.headers
    assert res.json == {"id": "one"}

    res = client.get("/many", headers={"accept": "application/json"})
    assert res.json == [{"id": "many"}]

    res = client.get("/one", headers={"accept": "application/xml"})
    assert res.status_code == 406
