# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
#
# Flask-Resources is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""JSON Deserializer."""

import json

from .deserializers import DeserializerMixin


class JSONDeserializer(DeserializerMixin):
    """JSON Deserializer."""

    def deserialize_data(self, data, *args, **kwargs):
        """Deserializes the input data into json."""
        return json.loads(data) if data else {}
