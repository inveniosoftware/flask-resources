# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
#
# Flask-Resources is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Library for easily implementing REST APIs."""
from functools import wraps

from flask import request
from marshmallow.validate import Range, Regexp
from webargs.fields import Int, String
from webargs.flaskparser import FlaskParser

from ..context import resource_requestctx
from .paginate import build_pagination


class ResourceFlaskParser(FlaskParser):
    """Customized FlaskParser for our needs."""

    DEFAULT_VALIDATION_STATUS = 400


def select_args_parser(resource_method, config_parser_or_parsers):
    """Returns ArgsParser corresponding to situation."""
    if isinstance(config_parser_or_parsers, ArgsParser):
        return config_parser_or_parsers

    # default "parse nothing" parser
    return config_parser_or_parsers.get(resource_method, ArgsParser())


def url_args_parser(f):
    """Decorator that parses the URL query string for the view.

    NOTE: Flask captures the query string on ``request.args`` ergo the compact name.
    """

    @wraps(f)
    def wrapper(self, *args, **kwargs):
        """Wrapping method.

        NOTE: To extract request args from any endpoint and not repeat ourselves,
              extraction is done here and inspects self + request.method to get
              endpoint.

        :params self: Item/List/SingletonView instance
        """
        # TODO: Create interfaces to not have to break Demeter's law here
        parser = select_args_parser(
            self.resource_method, self.resource.config.request_url_args_parser
        )
        resource_requestctx.request_args = parser.parse()
        return f(self, *args, **kwargs)

    return wrapper


class ArgsParser(object):
    """URL query string parser."""

    def __init__(self, argmap=None):
        """Constructor."""
        self.argmap = argmap

    def parse(self):
        """Parse."""
        # WARNING: This interface changes from webargs 5.5.3 (version we use) to
        # webargs 6.X (most recent webargs version). In 6.x it is
        # flaskparser.parse(self.argmap, request, location="querystring")
        if self.argmap is None:
            return {}
        flaskparser = ResourceFlaskParser()
        return flaskparser.parse(self.argmap, request, locations=("querystring",))


# TODO: Remove
class RequestParser:
    """RequestParser."""

    def __init__(self, fields=None, processors=None, *args, **kwargs):
        """Constructor."""
        self.fields = fields or {}
        self.processors = processors or []

    def parse(self, *args, **kwargs):
        """Parse."""
        flaskparser = ResourceFlaskParser()
        return self.post_process(
            flaskparser.parse(self.fields, request, *args, **kwargs)
        )

    def post_process(self, request_arguments, *args, **kwargs):
        """Post process."""
        for func in self.processors:
            func(request_arguments)
        return request_arguments


search_request_parser = RequestParser(
    fields={
        "page": Int(validate=Range(min=1), missing=1),
        "from": Int(validate=Range(min=1)),
        "size": Int(validate=Range(min=1), missing=10),
        "q": String(missing=""),
    },
    processors=[build_pagination],
)
