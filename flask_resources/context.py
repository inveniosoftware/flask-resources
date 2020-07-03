# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
#
# Flask-Resources is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Resource Request context."""

from functools import wraps

from flask import g, request
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

    def __init__(
        self, accept_mimetype=None, payload_mimetype=None, request_args=None, data=None,
    ):
        """Initialize the resource context."""
        self.accept_mimetype = accept_mimetype
        self.payload_mimetype = payload_mimetype  # Content-Type
        self.request_args = request_args
        self.request_content = data
        self.route = {}
        # Inject original request information into the context
        self.inject_original_request()

    def __enter__(self):
        """Push the resource context manager on the current request."""
        g.resource_requestctx = self

    def __exit__(self, type, value, traceback):
        """Pop the resource context manager from the current request."""
        del g.resource_requestctx

    def inject_original_request(self):
        """."""
        self.original_request = {
            'accept_mimetypes': request.accept_mimetypes,
            'args': request.args,
            'content_type': request.content_type,
            'data': request.data,
        }

    def update(self, values):
        """Update the context fields present in the received dictionary `values`."""
        for field, value in values.items():
            self.__setattr__(field, value)


def with_resource_requestctx(f):
    """Wrap in resource request context."""

    @wraps(f)
    def inner(self, *args, **kwargs):
        resource_request_context = getattr(
            self.resource.config, "context_class", ResourceRequestCtx)
        with resource_request_context():
            return f(self, *args, **kwargs)

    return inner


def with_route(f):
    """Wrapper to extract route arguments into resource context.

    NOTE: This removes the need for *args, **kwargs passing in Resource methods
    TODO: This should be temporary because the whole decorator approach should be
          revisited.
    """

    @wraps(f)
    def inner(*args, **kwargs):
        resource_requestctx.route = kwargs
        return f(*args)

    return inner
