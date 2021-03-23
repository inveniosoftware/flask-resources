# -*- coding: utf-8 -*-
#
# Copyright (C) 2020-2021 CERN.
# Copyright (C) 2020-2021 Northwestern University.
#
# Flask-Resources is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Library for implementing configurable REST APIs.

A resource is a factory for creating Flask Blueprint that's parameterized
via a config. The main difference from a regular blueprint is:

* Syntactical overlay - it creates a slightly different way of writing
  views and wiring them up with the Flask routing system. Flask-Resources
  is meant for REST APIs and thus puts emphasis on the HTTP method, and
  as apposed to a Flask MethodView, it allows keeping all view methods
  together for all endpoints.

* Dependency injection - a resource enables easy dependency injection via
  a configuration object. The idea behind this is for instance you write
  a reusable application that you want to allow developers to customize.
  For instance you could allow a developer to accept and deserialize their
  custom XML instead of only JSON at a given endpoint while keeping the
  application view the same, or allow them to customize the URL routes via
  the Flask application config.

In addition, Flask-Resources provides basic utilities for developing REST APIs
such as:

* Content negotiation to support multiple response serializations (e.g. serving
  JSON, JSON-LD, XML from the same endpoint).

* Request parsing (query string, headers, body) using Marshmallow and data
  deserialization.

* Resource request context to enforce paradigm of passing only validated
  request data to the view function.

If you don't need any of the above, you can simply use just a normal Flask
Blueprint instead.

Below is small minimal example:

.. code-block:: python

    from flask import Flask
    from flask_resources import Resource, ResourceConfig, route

    class Config(ResourceConfig):
        blueprint_name = "hello"

    class HelloWorldResource(Resource):
        def hello_world(self):
            return "Hello, World!"

        def create_url_rules(self):
            return [
                route("GET", "/", self.hello_world),
            ]

    app = Flask('test')
    app.config.update({
        "RESOURCE_CONFIG": Config()
    })
    resource = Resource(app.config["RESOURCE_CONFIG"])
    app.register_blueprint(resource.as_blueprint())


Larger example
--------------

Below is a large example that demonstrates:

- Response handling via content negotiation.
- Error handling and mapping of business-level exceptions to JSON errors.
- Request parsing from the body content, URL query string, headers and view
  args.
- Accessing the resource request context

.. code-block:: python

    class Config(ResourceConfig):
        # Response handlers defines possible mimetypes for content
        # negotiation
        response_handlers = {
            "application/json: ResponseHandler(JSONSerializer()),
            # ...
        }

    class MyResource(Resource):

        # Error handlers maps exceptions to JSON errors.
        error_handlers = {
            ma.ValidationError: create_error_handler(
                HTTPJSONException(code=400),
            )
        }

        decorators = [
            # You can apply decorators to all views
            login_required,
        ]

        @request_parser(
            {'q': ma.fields.String(required=True)},
            # Other locations include args, view_args, headers.
            location='args',
        )
        @response_handler(many=True)
        def search(self):
            # The validated data is available in the resource request context.
            if resource_requestctx.args['q']:
                # ...
            # From the view you can return an object which the response handler
            # will serialize.
            return [], 200

        # You can parse request body depending on the Content-Type header.
        @request_body(
            parsers={
                "application/json": RequestBodyParser(JSONDeserializer())
            }
        )
        @response_handler()
        def create(self):
            return {}, 201

        # All decorators all values to come from the conf.
        @request_parser(from_conf('update_args), location='args')
        def update(self):
            return {}, 201

        def create_url_rules(self):
            return [
                route('GET', "/", self.search),
                route('POST', "/", self.create),
                route('PUT', "/<pid_value>", self.update),
                # You can selectively disable global decorators.
                route('DELETE', "/<pid_value>", self.delete, apply_decorators=False),
            ]


"""

from .config import from_conf
from .content_negotiation import with_content_negotiation
from .context import resource_requestctx
from .deserializers import JSONDeserializer
from .errors import HTTPJSONException, create_error_handler
from .parsers import (
    MultiDictSchema,
    RequestBodyParser,
    RequestParser,
    request_body_parser,
    request_parser,
)
from .resources import Resource, ResourceConfig, route
from .responses import ResponseHandler, response_handler
from .serializers import JSONSerializer, MarshmallowJSONSerializer
from .version import __version__

__all__ = (
    "__version__",
    "create_error_handler",
    "from_conf",
    "HTTPJSONException",
    "JSONDeserializer",
    "JSONSerializer",
    "MarshmallowJSONSerializer",
    "MultiDictSchema",
    "request_body_parser",
    "request_parser",
    "RequestBodyParser",
    "RequestParser",
    "resource_requestctx",
    "Resource",
    "ResourceConfig",
    "response_handler",
    "ResponseHandler",
    "route",
    "with_content_negotiation",
)
