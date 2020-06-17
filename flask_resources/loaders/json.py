# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
#
# Flask-Resources is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""JSON loader."""

from flask import request

from .loaders import LoaderMixin


class JSONLoader(LoaderMixin):
    """JSON loader."""

    def load_request(self, *args, **kwargs):
        """Load the body of the request."""
        return request.get_json()
