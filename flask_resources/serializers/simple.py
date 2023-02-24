# -*- coding: utf-8 -*-
#
# Copyright (C) 2023 CERN.
#
# Flask-Resources is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Simple serializer."""

from .base import BaseSerializer


class SimpleSerializer(BaseSerializer):
    """Simple serializer implementation."""

    def __init__(self, encoder):
        """Initialize the SimpleSerializer."""
        self._encoder = encoder

    def serialize_object(self, obj, **kwargs):
        """Dump the object into a string using the encoder function."""
        return self._encoder(obj)

    def serialize_object_list(self, obj_list, **kwargs):
        """Dump the object list into a string separated by new lines."""
        # this is a coupled to the `BaseListSchema` or any other list schema that
        # returns its search results with this schema
        return "\n".join(
            [self.serialize_object(obj, **kwargs) for obj in obj_list["hits"]["hits"]]
        )
