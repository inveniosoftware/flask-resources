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


def _raw_args(*args, **kwargs):
    return {**request.headers}


class HeadersParser(RequestParser):
    """Headers parser."""

    location = "headers"
    raw_args_fn = _raw_args


headers_parser = request_parser_decorator(
    HeadersParser, "request_headers_parser", "headers"
)
