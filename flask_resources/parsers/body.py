# -*- coding: utf-8 -*-
#
# Copyright (C) 2020-2021 CERN.
# Copyright (C) 2020-2021 Northwestern University.
#
# Flask-Resources is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Request body parsers module."""

from flask import request


class RequestBodyParser:
    """Parse the request body."""

    def __init__(self, deserializer):
        """Constructor."""
        self.deserializer = deserializer

    def parse(self):
        """Parse the request body."""
        return self.deserializer.deserialize(request.data)
