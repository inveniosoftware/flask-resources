# -*- coding: utf-8 -*-
#
# Copyright (C) 2020-2021 CERN.
# Copyright (C) 2020-2021 Northwestern University.
#
# Flask-Resources is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Resource request context.

The purpose of the resource request context is similar to the Flask request
context. The main difference is it serves as a state object that can hold
validated request data as well as the result of e.g. content negotiation.

The resource request context is used by default, and when it is used it
consumes all the view arguments. These can either be retrieved via a request
parser (preferably), or accessing ``request.view_args``. The goal of this
is to ensure that the view function access only validated data.
"""

from functools import wraps
from inspect import ismethod

from flask import g
from werkzeug.local import LocalProxy


#
# Proxy to the current resource context
#
def _get_context():
    """Get the resource request context from the g object."""
    if hasattr(g, "resource_requestctx"):
        return g.resource_requestctx
    raise RuntimeError("Working outside of resource request context.")


resource_requestctx = LocalProxy(_get_context)
"""Proxy to the resource's request context"""


#
# Resource context
#
class ResourceRequestCtx(object):
    """Context manager for the resource context.

    The resource request context encodes information about the currently
    executing request for a given resource, such as:

    - The mimetype selected by the content negotiation.
    - The content type of the request payload
    """

    def __init__(self, config):
        """Initialize the resource context."""
        self.config = config
        self.args = None
        self.headers = None
        self.data = None
        self.view_args = None
        self.accept_mimetype = None
        self.response_handler = None

    def __enter__(self):
        """Push the resource context manager on the current request."""
        g.resource_requestctx = self

    def __exit__(self, type, value, traceback):
        """Pop the resource context manager from the current request."""
        del g.resource_requestctx

    def update(self, values):
        """Update the context fields present in the received dictionary `values`."""
        for field, value in values.items():
            self.__setattr__(field, value)
