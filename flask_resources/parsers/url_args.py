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
    return request.args.to_dict(flat=False)


class URLArgsParser(RequestParser):
    """URL query string parser."""

    location = "querystring"
    raw_args_fn = _raw_args


url_args_parser = request_parser_decorator(
    URLArgsParser,
    "request_url_args_parser",
    "url_args",
)
