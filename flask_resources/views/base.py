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

from ..context import with_resource_requestctx


class BaseView(MethodView):
    """Base view."""

    with_context_decorator = True
    """Flag to control resource context pushing decorator."""

    def __init__(self, resource, *args, **kwargs):
        super(BaseView, self).__init__(*args, **kwargs)
        self.resource = resource
        if self.with_context_decorator:
            # Push the decorator to the end, so that it's applied before any
            # other decorator.
            self.decorators += (with_resource_requestctx,)
