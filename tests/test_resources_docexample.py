# SPDX-FileCopyrightText: 2020-2021 CERN.
# SPDX-FileCopyrightText: 2020-2021 Northwestern University.
# SPDX-License-Identifier: MIT

"""Resources test module."""

import pytest
from flask import Flask

from flask_resources import Resource, ResourceConfig, route


@pytest.fixture(scope="module")
def app():
    """Doc example app."""

    class Config(ResourceConfig):
        blueprint_name = "hellow"

    class HelloWorldResource(Resource):
        def hello_world(self):
            return "Hello, World!"

        def create_url_rules(self):
            return [
                route("GET", "/", self.hello_world),
            ]

    app = Flask("test")
    app.config.update({"RESOURCE_CONFIG": Config()})
    resource = HelloWorldResource(app.config["RESOURCE_CONFIG"])
    app.register_blueprint(resource.as_blueprint())
    return app


def test_doc_example(client):
    assert client.get("/").get_data(as_text=True) == "Hello, World!"
