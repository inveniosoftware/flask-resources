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
from marshmallow.validate import Range, Regexp
from webargs.fields import Int, String
from webargs.flaskparser import FlaskParser

from ..context import resource_requestctx


class ResourceFlaskParser(FlaskParser):
    """Customized FlaskParser for our needs."""

    DEFAULT_VALIDATION_STATUS = 400


def select_args_parser(resource_method, config_parser_or_parsers):
    """Returns ArgsParser corresponding to situation."""
    if isinstance(config_parser_or_parsers, ArgsParser):
        return config_parser_or_parsers

    return config_parser_or_parsers.get(
        resource_method,
        ArgsParser(allow_unknown=False),  # default "parse nothing" parser
    )


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

    def __init__(self, argmap=None, allow_unknown=True):
        """Constructor.

        :params argmap: dict or Schema of URL querystring arguments
        :params allow_unknown: bool allow unknown URL querystring arguments or not
        """
        self.argmap = argmap or {}
        self.allow_unknown = allow_unknown

    def parse(self):
        """Parse."""
        # NOTE: This has to be done bc webargs 5.X < 6.X doesn't obey schemas that
        #       allow unknown fields. webargs 6.X does, so this can be changed when
        #       upgrading dependencies
        raw_args = request.args.to_dict(flat=False) if self.allow_unknown else {}
        flaskparser = ResourceFlaskParser()
        # WARNING: This interface changes from webargs 5.5.3 (version we use) to
        #          webargs 6.X (most recent webargs version). In 6.x it is
        #          flaskparser.parse(self.argmap, request, location="querystring")
        parsed_args = flaskparser.parse(
            self.argmap, request, locations=("querystring",)
        )
        return {**raw_args, **parsed_args}
