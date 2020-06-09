# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
#
# Flask-Resources is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""Flask Resources module to create REST APIs."""

from ..args.parsers import item_request_parser
from .base import BaseView


class SingletonView(BaseView):
    """Parse request args and create a request context.

    Note that the resource route should contain the `<id>` param.
    """

    def __init__(
        self, resource=None, item_parser=item_request_parser, *args, **kwargs
    ):
        super(SingletonView, self).__init__(resource=resource, *args, **kwargs)
        self.item_parser = item_parser

    def post(self, *args, **kwargs):
        return self.resource.create()

    def get(self, *args, **kwargs):
        return self.resource.read()

    def put(self, *args, **kwargs):
        return self.resource.update()

    def patch(self, *args, **kwargs):
        return self.resource.partial_update()

    def delete(self, *args, **kwargs):
        return self.resource.delete()
