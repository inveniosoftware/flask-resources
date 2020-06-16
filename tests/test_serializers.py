# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
#
# Flask--Resources is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""Serializers test module."""

import json

from werkzeug.exceptions import HTTPException

from flask_resources.serializers import JSONSerializer, SerializerMixin


class CustomSerializer(SerializerMixin):
    """Custom serializer implementation."""

    def serialize_object(self, object, response_ctx=None, *args, **kwargs):
        """Dump the object into a json string."""
        return object.get("content")

    def serialize_object_list(self, object_list, response_ctx=None, *args, **kwargs):
        """Dump the object list into a json string."""
        return str([obj.get("content") for obj in object_list])

    def serialize_error(self, error, response_ctx=None, *args, **kwargs):
        """Serialize an error reponse according to the response ctx."""
        # NOTE: In non-overwritten exceptions (i.e. coming from Werkzeug)
        # `get_description` returns HTML tags.
        return error.description


def test_custom_serializer():
    """Test custom serializer."""
    serializer = CustomSerializer()

    # Test a simple object
    obj = {"id": "value", "content": "another value"}
    assert serializer.serialize_object(obj) == obj.get("content")

    # Test an object list
    obj_list = [obj, obj, obj]
    assert serializer.serialize_object_list(obj_list) == str(
        [obj.get("content") for obj in obj_list]
    )

    # Test an exception
    error = HTTPException()
    assert serializer.serialize_error(error) == error.description


def test_json_serializer():
    """Test JSON serializer."""
    serializer = JSONSerializer()

    # Test a simple object
    obj = {"field_one": "value", "field_two": "another value"}
    assert serializer.serialize_object(obj) == json.dumps(obj)

    # Test an object list
    obj_list = [obj, obj, obj]
    assert serializer.serialize_object_list(obj_list) == json.dumps(obj_list)

    # Test an exception
    error = HTTPException()
    assert serializer.serialize_error(error) == json.dumps(error.description)
