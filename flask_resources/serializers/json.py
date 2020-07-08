# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
# Copyright (C) 2020 Northwestern University.
#
# Flask-Resources is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""JSON serializer."""

import json

from .serializers import SerializerMixin


class JSONSerializer(SerializerMixin):
    """JSON serializer implementation."""

    def serialize_object(self, obj, response_ctx=None, *args, **kwargs):
        """Dump the object into a json string."""
        return json.dumps(obj)

    def serialize_object_list(self, obj_list, response_ctx=None, *args, **kwargs):
        """Dump the object list into a json string."""
        return json.dumps(obj_list)
