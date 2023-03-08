# -*- coding: utf-8 -*-
#
# Copyright (C) 2020-2023 CERN.
# Copyright (C) 2020-2021 Northwestern University.
#
# Flask-Resources is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""JSON serializer."""

import json
import warnings

from flask import request
from flask.json.provider import _default
from speaklater import is_lazy_string

from .base import BaseSerializer, MarshmallowSerializer


def flask_request_options():
    """Options to pretty print the JSON."""
    if request and request.args.get("prettyprint"):
        return {
            "indent": 2,
            "sort_keys": True,
        }
    return {}


class JSONEncoder(json.JSONEncoder):
    """JSONEncoder for our custom needs.

    - Knows to force translate lazy translation strings.
    """

    def default(self, obj):
        """Override parent's default."""
        if is_lazy_string(obj):
            return str(obj)
        return _default(obj)


class JSONSerializer(BaseSerializer):
    """JSON serializer implementation."""

    def __init__(self, encoder=None, options=None):
        """Initialize the JSONSerializer."""
        self._options = options or flask_request_options
        self._encoder = encoder or JSONEncoder

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
        return json.dumps(obj, cls=self.encoder, **self.dumps_options)

    def serialize_object_list(self, obj_list):
        """Dump the object list into a json string."""
        return json.dumps(obj_list, cls=self.encoder, **self.dumps_options)
