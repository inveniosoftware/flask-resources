# -*- coding: utf-8 -*-
#
# Copyright (C) 2020-2021 CERN.
# Copyright (C) 2020-2021 Northwestern University.
#
# Flask-Resources is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Header parser."""

from flask import request

from .base import RequestParser, request_parser_decorator


class HeadersParser(RequestParser):
    """Headers parser."""

    def load_data(self):
        """Load data from headers."""
        return {k.lower().replace("-", "_"): v for (k, v) in request.headers.items()}


headers_parser = request_parser_decorator(
    HeadersParser,
    # Attribute name on the resource config
    "request_headers_parser",
    # Attribute name on the resource_requestctx
    "headers",
)
