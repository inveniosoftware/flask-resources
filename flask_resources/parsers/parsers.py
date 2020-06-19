# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
#
# Flask-Resources is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Library for easily implementing REST APIs."""

from flask import request
from marshmallow.validate import Range, Regexp
from webargs.fields import Int, String
from webargs.flaskparser import parser

from .paginate import build_pagination


class RequestParser:
    """RequestParser."""

    def __init__(self, fields=None, processors=None, *args, **kwargs):
        """Constructor."""
        self.fields = fields or {}
        self.processors = processors or []

    def parse(self, *args, **kwargs):
        """Parse."""
        return self.post_process(parser.parse(self.fields, request, *args, **kwargs))

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
