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
    JSONDeserializer,
    RequestBodyParser,
    Resource,
    ResourceConfig,
    request_body_parser,
    resource_requestctx,
    route,
)


@pytest.fixture(scope="module")
def resource():
    class TestConfig(ResourceConfig):
        blueprint_name = "test"

    class TestResource(Resource):
        @request_body_parser(
            parsers={
                "application/vnd.1": RequestBodyParser(deserializer=JSONDeserializer())
            }
        )
        def index(self):
            return resource_requestctx.data["val"], 200

        def create_url_rules(self):
            return [
                route("PUT", "/", self.index),
            ]

    return TestResource(TestConfig)


def test_body_parser(client):
    res = client.put(
        "/",
        headers={"content-type": "application/vnd.1"},
        data=json.dumps({"val": "1"}),
    )
    assert res.get_data(as_text=True) == "1"

    res = client.put(
        "/",
        headers={"content-type": "application/invalid"},
        data=json.dumps({"val": "1"}),
    )
    assert res.status_code == 415
