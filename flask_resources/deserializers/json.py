# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
#
# Flask-Resources is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""JSON Deserializer."""

from .deserializer import DeserializerMixin


class JSONDeserializer(DeserializerMixin):
    """JSON Deserializer."""

    def deserialize_object(self, obj, *args, **kwargs):
        """Deserializes an object into json."""
        return json.loads(obj)
