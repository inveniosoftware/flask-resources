# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
# Copyright (C) 2020 Northwestern University.
#
# Flask-Resources is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""JSON serializer."""

import json

from flask import request

from ..json_encoder import CustomJSONEncoder
from .serializers import SerializerMixin


def flask_request_options():
    """Options to pretty print the JSON."""
    if request and request.args.get("prettyprint"):
        return {
            "indent": 2,
            "sort_keys": True,
        }
    return {}


class JSONSerializer(SerializerMixin):
    """JSON serializer implementation."""

    def __init__(self, encoder=None, options=None):
        """Initialize the JSONSerializer."""
        self._options = options or flask_request_options
        self._encoder = encoder or CustomJSONEncoder

    @property
    def dumps_options(self):
        """Support adding options for the dumps() method."""
        return self._options() if callable(self._options) else self._options

    @property
    def encoder(self):
        """Support overriding the JSONEncoder used for serialization."""
        # We let classes through as-is
        if isinstance(self._encoder, type):
            return self._encoder
        elif callable(self._encoder):
            return self._encoder()
        return self._encoder

    def serialize_object(self, obj):
        """Dump the object into a json string."""
        encoder = self.encoder
        return json.dumps(obj, cls=encoder, **self.dumps_options)

    def serialize_object_list(self, obj_list):
        """Dump the object list into a json string."""
        return json.dumps(obj_list, cls=self.encoder, **self.dumps_options)


class MarshmallowJSONSerializer(JSONSerializer):
    """JSON serializing using Marshmallow to transform output."""

    def __init__(self, item_schema=None, list_schema=None, **kwargs):
        """Initialize the serializer."""
        self._item_schema_cls = item_schema
        self._list_schema_cls = list_schema
        super().__init__(**kwargs)

    def serialize_object(self, obj):
        """Dump the object into a JSON string."""
        return super().serialize_object(self.dump_item(obj))

    def serialize_object_list(self, obj_list):
        """Dump the object list into a JSON string."""
        return super().serialize_object_list(self.dump_list(obj_list))

    def dump_item(self, obj):
        """Dump the object with extra information."""
        return self._item_schema_cls().dump(obj)

    def dump_list(self, obj_list):
        """Dump the list of objects with extra information."""
        ctx = {
            "item_schema_cls": self._item_schema_cls,
        }
        return self._list_schema_cls(context=ctx).dump(obj_list)
