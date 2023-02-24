# -*- coding: utf-8 -*-
#
# Copyright (C) 2023 CERN.
#
# Flask-Resources is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""XML serializer."""

from .base import SerializerMixin


class XMLSerializer(SerializerMixin):
    """XML serializer implementation."""

    def __init__(self, string_encoder):
        """Initialize the JSONSerializer."""
        self._string_encoder = string_encoder

    def serialize_object(self, obj, **kwargs):
        """Dump the object into a xml string."""
        return self._string_encoder(obj)

    def serialize_object_list(self, obj_list, **kwargs):
        """Dump the object list into a xml string."""
        # this is a coupled to the `BaseListSchema` or any other list schema that
        # returns its search results with this schema
        return "\n".join(
            [self.serialize_object(obj, **kwargs) for obj in obj_list["hits"]["hits"]]
        )
