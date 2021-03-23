# -*- coding: utf-8 -*-
#
# Copyright (C) 2020-2021 CERN.
# Copyright (C) 2020-2021 Northwestern University.
#
# Flask-Resources is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Resource view."""

from inspect import ismethod

from flask import Blueprint
from werkzeug.exceptions import HTTPException

from .config import from_conf, resolve_from_conf
from .content_negotiation import with_content_negotiation
from .context import ResourceRequestCtx
from .deserializers import JSONDeserializer
from .errors import handle_http_exception
from .parsers import RequestBodyParser
from .responses import ResponseHandler
from .serializers import JSONSerializer


def route(
    method,
    rule,
    view_meth,
    endpoint=None,
    rule_options={},
    apply_decorators=True,
):
    """Create a route.

    Use this method in ``create_url_rules()`` to build your list of rules.

    The ``view_method`` parameter should be a bound method (e.g.
    ``self.myview``).

    :param method: The HTTP method for this URL rule.
    :param rule: A URL rule.
    :param view_meth: The view method (a bound method) for this URL rule.
    :param endpoint: The name of the endpoint. By default the name is taken
        from the method name.
    :param rule_options: A dictionary of extra options passed to
        ``Blueprint.add_url_rule``.
    :param apply_decorators: Apply the decorators defined by the resource.
        Defaults to ``True``. This allows you to selective disable
        decorators which are normally applied to all view methods.
    """
    view_name = view_meth.__name__
    config = view_meth.__self__.config
    decorators = view_meth.__self__.decorators

    if apply_decorators:
        # reversed so order is the same as when applied directly to method
        for decorator in reversed(decorators):
            view_meth = decorator(view_meth)

    def view(*args, **kwargs):
        with ResourceRequestCtx(config):
            # args and kwargs are ignored on purpose - use a request parser
            # to retrieve the validated values.
            return view_meth()

    view.__name__ = view_name

    return {
        "rule": resolve_from_conf(rule, config),
        "methods": [method],
        "view_func": view,
        "endpoint": endpoint,
        **rule_options,
    }


class ResourceConfig:
    """Configuration for a resource.

    This object is used for dependency injection in a resource.
    """

    # Blueprint options and routing
    # =============================

    #: Name of the blueprint being created (used e.g. for prefix endpoint name).
    blueprint_name = None
    #: The URL prefix for the blueprint (all URL rules will be prefixed with this value)
    url_prefix = None
    #: A mapping of exception or HTTP status code to error handler functions.
    error_handlers = {}

    # Request parsing
    # ===============

    #: Request body parser (i.e. ``request.data``).
    request_body_parsers = {"application/json": RequestBodyParser(JSONDeserializer())}
    #: The default content type used to select the default request_body_parser.
    #: Set to ``None`` to require a Content-Type header.
    default_content_type = "application/json"

    # Response handling
    # =================

    #: Mapping of Accept MIME types to response handlers.
    response_handlers = {"application/json": ResponseHandler(JSONSerializer())}
    #: The default Accept MIME type if not defined by the request.
    #: Set to ``None``, to require an Accept header.
    default_accept_mimetype = "application/json"


class Resource:
    """Resource interface.

    A resource is a factory for creating Flask Blueprint that's parameterized
    via a config.
    """

    decorators = [
        with_content_negotiation(
            response_handlers=from_conf("response_handlers"),
            default_accept_mimetype=from_conf("default_accept_mimetype"),
        )
    ]
    """Decorators applied to all view functions.

    By default, the resource request context and content negotiation is
    enabled. Provide an empty list to disable them.
    """

    error_handlers = {}
    """Mapping of exceptions or HTTP codes to error handler functions.

    By default this mapping is merged with the error handlers mapping defined
    in the config.
    """

    def __init__(self, config):
        """Initialize the base resource."""
        self.config = config

    def as_blueprint(self, **options):
        """Create the blueprint with all views and error handlers.

        The method delegates to ``create_blueprint()``, ``create_url_rules()``
        and ``create_error_handlers()`` so usually you don't have to overwrite
        this method.
        """
        blueprint = self.create_blueprint(**options)

        for rule in self.create_url_rules():
            blueprint.add_url_rule(**rule)

        for exc_or_code, error_handler in self.create_error_handlers():
            blueprint.register_error_handler(exc_or_code, error_handler)

        return blueprint

    def create_blueprint(self, **options):
        """Create the blueprint.

        Override this function to customize the creation of the ``Blueprint``
        object itself.
        """
        if hasattr(self.config, "url_prefix"):
            options.setdefault("url_prefix", self.config.url_prefix)
        return Blueprint(self.config.blueprint_name, __name__, **options)

    def create_url_rules(self):
        """Create all the blueprint URL rules for this resource.

        The URL rules are registered on the blueprint using the
        ``Blueprint.add_url_rule()``.
        """
        return []

    def create_error_handlers(self):
        """Create all error handlers for this resource.

        This function should return a dictionary that maps an exception or HTTP
        response code to and error handler function. By default it merges
        error handlers defined on the resource itself with error handlers
        defined in the config. The error handlers in the config takes
        precedence over the resource defined error handlers.

        The error handlers are registered on the blueprint using the
        ``Blueprint.register_error_handler()``.
        """
        error_handlers = {
            HTTPException: handle_http_exception,
        }
        error_handlers.update(self.error_handlers)
        error_handlers.update(self.config.error_handlers)

        return error_handlers.items()
