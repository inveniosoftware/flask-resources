# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
# Copyright (C) 2020 Northwestern University.
#
# Flask-Resources is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Library for easily implementing REST APIs."""

from functools import wraps

from flask import request
from webargs.flaskparser import FlaskParser

from ..context import resource_requestctx


def _raw_args(*args, **kwargs):
    return {}


def select_request_parser(
    resource_method, config_parser_or_parsers, default_parser_cls
):
    """Returns request parser corresponding to situation."""
    if isinstance(config_parser_or_parsers, default_parser_cls):
        return config_parser_or_parsers

    return config_parser_or_parsers.get(
        resource_method,
        default_parser_cls(allow_unknown=False),  # default "parse nothing" parser
    )


def request_parser_decorator(parser_cls, config_attr, context_attr):
    """Decorator that parses the request object for the view."""

    def decorator(f):
        @wraps(f)
        def inner(self, *args, **kwargs):
            parser = select_request_parser(
                self.resource_method,
                getattr(self.resource.config, config_attr),
                parser_cls,
            )
            setattr(resource_requestctx, context_attr, parser.parse())
            return f(self, *args, **kwargs)

        return inner

    return decorator


class ResourceFlaskParser(FlaskParser):
    """Customized FlaskParser for our needs."""

    DEFAULT_VALIDATION_STATUS = 400


class RequestParser(object):
    """Request parser.

    The class is defining the following attributes:
    str location: Where on the request to search for values.
        Can include one of ``('json', 'querystring', 'form',
        'headers', 'cookies', 'files')``.
    raw_args_fn: Function to return raw arguments from the current request
        object being parsed.
    """

    location = None
    raw_args_fn = _raw_args

    def __init__(self, argmap=None, allow_unknown=True):
        """Constructor.

        :param argmap: Either a `marshmallow.Schema`, a `dict`
            of argname -> `marshmallow.fields.Field` pairs, or a callable
            which accepts a request and returns a `marshmallow.Schema`.
        :params bool allow_unknown: Allow unknown fields i.e not declared to
            the `argsmap`, to be parsed.
        """
        self.argmap = argmap or {}
        self.allow_unknown = allow_unknown

    def parse(self):
        """Parse."""
        # NOTE: This has to be done bc webargs 5.X < 6.X doesn't obey schemas that
        #       allow unknown fields. webargs 6.X does, so this can be changed when
        #       upgrading dependencies
        raw_args = self.raw_args_fn() if self.allow_unknown else {}
        flaskparser = ResourceFlaskParser()
        # WARNING: This interface changes from webargs 5.5.3 (version we use) to
        #          webargs 6.X (most recent webargs version). In 6.x it is
        #          flaskparser.parse(self.argmap, request, location="querystring")
        parsed_args = flaskparser.parse(
            self.argmap, request, locations=(self.location,)
        )
        return {**raw_args, **parsed_args}
