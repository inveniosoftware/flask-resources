# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
# Copyright (C) 2020 Northwestern University.
#
# Flask-Resources is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Load headers in resource_requestctx."""

from functools import wraps

from flask import request

from .context import resource_requestctx


class HeadersParser:
    """Identity headers parser."""

    def parse(self, headers):
        """Parses a request's headers.

        Different parsers would override this. Otherwise, this parser just
        returns the headers.
        """
        return headers


def headers_decorator(f):
    """Decorator that parses the request's headers for the view."""

    @wraps(f)
    def wrapper(self, *args, **kwargs):
        """Wrapping method.

        NOTE: To extract request args from any endpoint and not repeat ourselves,
              extraction is done here and inspects self + request.method to get
              endpoint.

        :params self: Item/List/SingletonView instance
        """
        # TODO: Select a headers parser based on method
        parser = HeadersParser()
        resource_requestctx.headers = parser.parse(request.headers)
        return f(self, *args, **kwargs)

    return wrapper
