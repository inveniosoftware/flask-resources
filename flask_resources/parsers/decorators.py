# -*- coding: utf-8 -*-
#
# Copyright (C) 2020-2021 CERN.
# Copyright (C) 2020-2021 Northwestern University.
#
# Flask-Resources is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Decorator for invoking the request parser."""

import warnings
from functools import wraps

from flask import request

from flask_resources.deserializers.json import JSONDeserializer

from ..config import resolve_from_conf
from ..context import resource_requestctx
from ..errors import InvalidContentType
from .base import RequestParser
from .body import RequestBodyParser


def request_parser(schema_or_parser, location=None, **options):
    """Create decorator for parsing the request.

    Both decorator parameters can be resolved from the resource configuration.

    :param schema_or_parser: A mapping of content types to parsers.
    :param default_content_type_name: The default content type used to select
        a parser if no content type was provided.
    """

    def decorator(f):
        @wraps(f)
        def inner(self, *args, **kwargs):
            s = resolve_from_conf(schema_or_parser, self.config)
            if isinstance(s, RequestParser):
                parser = s
                if location is not None:
                    warnings.warn("The location is ignored.")
            else:
                parser = RequestParser(s, location, **options)

            ctx_attr = getattr(resource_requestctx, parser.location)
            if ctx_attr is None:
                setattr(resource_requestctx, parser.location, parser.parse())
            else:
                ctx_attr.update(parser.parse())
            return f(self, *args, **kwargs)

        return inner

    return decorator


def request_body_parser(
    parsers={"application/json": RequestBodyParser(deserializer=JSONDeserializer())},
    default_content_type="application/json",
):
    """Create decorator for parsing the request body.

    Both decorator parameters can be resolved from the resource configuration.

    :param parsers: A mapping of content types to parsers.
    :param default_content_type_name: The default content type used to select
        a parser if no content type was provided.
    """

    def decorator(f):
        @wraps(f)
        def inner(self, *args, **kwargs):
            # Get the possible parsers
            body_parsers = resolve_from_conf(parsers, self.config)

            # Get the request body content type
            content_type = request.content_type or resolve_from_conf(
                default_content_type, self.config
            )

            # Get the parser
            parser = body_parsers.get(content_type)
            if parser is None:
                raise InvalidContentType(allowed_mimetypes=body_parsers.keys())

            # Parse the request body.
            resource_requestctx.data = parser.parse()

            return f(self, *args, **kwargs)

        return inner

    return decorator
