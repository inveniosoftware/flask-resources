# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
# Copyright (C) 2020 Northwestern University.
#
# Flask-Resources is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""Test deserialization."""

import marshmallow as ma
from flask import Flask, request
from speaklater import make_lazy_string

from flask_resources.serializers import JSONSerializer, MarshmallowJSONSerializer


def _(s):
    return make_lazy_string(lambda: s)


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
    class TestSchema(ma.Schema):
        title = ma.fields.Str(data_key="test")

    s = MarshmallowJSONSerializer(schema_cls=TestSchema)
    assert s.serialize_object({"title": "a"}) == '{"test": "a"}'
    assert s.serialize_object_list([{"title": "a"}]) == '[{"test": "a"}]'
