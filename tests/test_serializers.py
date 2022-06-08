# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
# Copyright (C) 2020 Northwestern University.
#
# Flask-Resources is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""Test deserialization."""

from flask import Flask
from marshmallow import Schema, fields
from speaklater import make_lazy_string

from flask_resources import (
    BaseListSchema,
    BaseObjectSchema,
    MarshmallowJSONSerializer,
    MarshmallowSerializer,
)
from flask_resources.serializers import JSONSerializer


def _(s):
    return make_lazy_string(lambda: s)


class UITestSchema(BaseObjectSchema):
    test = fields.String(dump_only=True)


def test_lazy_strings_are_serialized():
    serializer = JSONSerializer()
    lazy = {"key": _("Lazy")}
    list_lazy = [{"key": _("Lazy1")}, {"key": _("Lazy2")}]

    assert '{"key": "Lazy"}' == serializer.serialize_object(lazy)
    assert '[{"key": "Lazy1"}, {"key": "Lazy2"}]' == serializer.serialize_object_list(
        list_lazy
    )


def test_prettyprint():
    app = Flask("test")
    with app.test_request_context("/?prettyprint=1"):
        serializer = JSONSerializer()
        assert '{\n  "key": "1"\n}' == serializer.serialize_object({"key": "1"})


def test_marhsmallow_serializer():
    class TestSchema(Schema):
        title = fields.Str(data_key="test")

    s = MarshmallowJSONSerializer(schema_cls=TestSchema)
    assert s.serialize_object({"title": "a"}) == '{"test": "a"}'
    assert s.serialize_object_list([{"title": "a"}]) == '[{"test": "a"}]'


def test_marshmallow_serializer_without_context():
    serializer = MarshmallowSerializer(
        format_serializer_cls=JSONSerializer,
        object_schema_cls=UITestSchema,
        list_schema_cls=BaseListSchema,
    )
    test = {"test": _("test")}

    assert serializer.serialize_object(test) == '{"test": "test"}'


def test_marshmallow_serializer_with_context():
    serializer = MarshmallowSerializer(
        format_serializer_cls=JSONSerializer,
        object_schema_cls=UITestSchema,
        list_schema_cls=BaseListSchema,
        schema_context={"object_key": "ui"},
    )
    test = {"test": _("test")}
    assert (
        serializer.serialize_object(test) == '{"test": "test", "ui": {"test": "test"}}'
    )
