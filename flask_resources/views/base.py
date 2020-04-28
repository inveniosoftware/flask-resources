# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
#
# Flask-Resources is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""Flask Resources module to create REST APIs.

The views responsabilities are:
- Parse request arguments.
- Build a request context for the resource.
"""

from flask.views import MethodView
from functools import wraps

from ..context import ResourceRequestCtx


def with_resource_requestctx(f):
    @wraps(f)
    def inner(*args, **kwargs):
        with ResourceRequestCtx() as request_context:
            return f(*args, **kwargs)

    return inner


class BaseView(MethodView):
    """Base view."""

    def __init__(self, resource, *args, **kwargs):
        super(BaseView, self).__init__(*args, **kwargs)
        self.resource = resource
