# -*- coding: utf-8 -*-
#
# Copyright (C) 2020-2021 CERN.
# Copyright (C) 2020-2021 Northwestern University.
#
# Flask-Resources is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""JSON Deserializer."""

import json

from .base import DeserializerMixin


class JSONDeserializer(DeserializerMixin):
    """JSON Deserializer."""

    def deserialize(self, data):
        """Deserializes JSON into a Python dictionary."""
        return json.loads(data) if data else None
