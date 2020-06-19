# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
#
# Flask-Resources is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""Flask Resources module to create REST APIs."""

from .base import BaseView


class SingletonView(BaseView):
    """Parse request args and create a request context.

    Note that the resource route should contain the `<id>` param.
    """

    def __init__(self, resource=None, *args, **kwargs):
        """Constructor."""
        super(SingletonView, self).__init__(resource=resource, *args, **kwargs)

    def post(self, *args, **kwargs):
        """Post."""
        return self.resource.create()

    def get(self, *args, **kwargs):
        """Get."""
        return self.resource.read()

    def put(self, *args, **kwargs):
        """Put."""
        return self.resource.update()

    def patch(self, *args, **kwargs):
        """Patch."""
        return self.resource.partial_update()

    def delete(self, *args, **kwargs):
        """Delete."""
        return self.resource.delete()
