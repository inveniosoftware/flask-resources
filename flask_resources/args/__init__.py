# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
#
# Flask-Resources is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Library for easily implementing REST APIs."""

from .parsers import (
    RequestParser,
    create_request_parser,
    item_request_parser,
    search_request_parser,
)

__all__ = (
    "RequestParser",
    "create_request_parser",
    "item_request_parser",
    "search_request_parser",
)
