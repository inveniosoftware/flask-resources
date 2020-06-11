# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
#
# Flask-Resources is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Library for easily implementing REST APIs."""

from flask import request
from flask_resources.args.paginate import build_pagination
from marshmallow.validate import Range, Regexp
from webargs.fields import Int, String
from webargs.flaskparser import parser


class RequestParser:
    def __init__(self, fields=None, processors=None):
        self.fields = fields or {}
        self.processors = processors or []

    def parse(self):
        return self.post_process(
            parser.parse(self.fields, request, locations=["view_args"])
        )

    def post_process(self, request_arguments):
        for func in self.processors:
            func(request_arguments)
        return request_arguments


search_request_parser = RequestParser(
    fields={
        "page": Int(validate=Range(min=1),),
        "from": Int(load_from="from", validate=Range(min=1),),
        "size": Int(validate=Range(min=1), missing=10,),
        "q": String(),  # TODO: allow getting it from "query" maybe a Function
    },
    processors=[build_pagination],
)

create_request_parser = RequestParser()

item_request_parser = RequestParser(fields={"id": String(required=True)})
