# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
# Copyright (C) 2020 Northwestern University.
#
# Flask-Resources is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Library for easily implementing REST APIs."""

from flask import request

from .base import RequestParser, request_parser_decorator
from .schema import MultiDictSchema


class URLArgsParser(RequestParser):
    """URL query string parser."""

    DEFAULT_SCHEMA_CLASS = MultiDictSchema

    def __init__(self, *args, **kwargs):
        """Initialize the arguments parser.

        :param schema: The marshmallow schema class or a dictionary of fields.
        :param as_dict: If ``False``, the schema is passed a MultiDict object and
            must be able to handle it (see
            ``flask_resources.parsers.MultiDictSchema``). If True, the schema
            is passed a dictionary where the values are lists.
        """
        self.as_dict = kwargs.pop("as_dict", False)
        super().__init__(*args, **kwargs)

    def load_data(self):
        """Load data from the request args."""
        if self.as_dict:
            return request.args.to_dict(flat=False)
        else:
            return request.args


url_args_parser = request_parser_decorator(
    URLArgsParser,
    # Attribute name on the resource config
    "request_url_args_parser",
    # Attribute name on the resource_requestctx
    "url_args",
)
