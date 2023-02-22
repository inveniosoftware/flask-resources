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
        data = self.dump_obj(obj, **kwargs)
        return self.string_encoder(data)

    def serialize_object_list(self, obj_list, **kwargs):
        """Dump the object list into a xml string."""
        # this is a coupled to the `BaseListSchema` or any other list schema that
        # returns its search results with this schema
        return "\n".join(obj_list["hits"]["hits"])
