# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
# Copyright (C) 2020 Northwestern University.
#
# Flask-Resources is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Library for easily implementing REST APIs."""

from .headers import HeadersParser, headers_parser
from .schema import MultiDictSchema
from .url_args import URLArgsParser, url_args_parser

__all__ = (
    "headers_parser",
    "HeadersParser",
    "MultiDictSchema",
    "url_args_parser",
    "URLArgsParser",
)
