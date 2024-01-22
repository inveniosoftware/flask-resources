# -*- coding: utf-8 -*-
#
# Copyright (C) 2020-2024 CERN.
# Copyright (C) 2020 Northwestern University.
#
# Flask-Resources is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""Test serialization."""

from flask import Flask
from marshmallow import fields
from speaklater import make_lazy_string

from flask_resources import BaseListSchema, BaseObjectSchema, MarshmallowSerializer
from flask_resources.serializers import CSVSerializer, JSONSerializer, SimpleSerializer


def _(s):
    return make_lazy_string(lambda: s)


def dummy_xml_encoder(obj):
    xml = "<root>"
    for key, value in obj.items():
        xml += f"<{key}>{value}</{key}>"

    xml += "</root>"
    return xml


class UITestSchema(BaseObjectSchema):
    test = fields.String(dump_only=True, data_key="title_l10n")


def test_lazy_strings_are_serialized():
    serializer = JSONSerializer()
    lazy = {"key": _("Lazy")}
    list_lazy = [{"key": _("Lazy1")}, {"key": _("Lazy2")}]

    assert '{"key": "Lazy"}' == serializer.serialize_object(lazy)
    assert '[{"key": "Lazy1"}, {"key": "Lazy2"}]' == serializer.serialize_object_list(
        list_lazy
    )


def test_xml_serializer_object():
    serializer = SimpleSerializer(dummy_xml_encoder)

    obj = {"test": "one", "also": "test"}
    assert (
        "<root><test>one</test><also>test</also></root>"
        == serializer.serialize_object(obj)
    )


def test_xml_serializer_object_list():
    serializer = SimpleSerializer(dummy_xml_encoder)

    obj = {
        "hits": {
            "hits": [{"test": "one", "also": "test"}, {"test": "two", "also": "test"}]
        }
    }
    assert (
        "<root><test>one</test><also>test</also></root>\n<root><test>two</test><also>test</also></root>"
        == serializer.serialize_object_list(obj)
    )


def test_prettyprint():
    app = Flask("test")
    with app.test_request_context("/?prettyprint=1"):
        serializer = JSONSerializer()
        assert '{\n  "key": "1"\n}' == serializer.serialize_object({"key": "1"})


def test_marshmallow_json_serializer_without_context():
    serializer = MarshmallowSerializer(
        format_serializer_cls=JSONSerializer,
        object_schema_cls=UITestSchema,
        list_schema_cls=BaseListSchema,
    )
    test = {"test": _("test")}
    list_test = {"hits": {"hits": [{"test": _("test1")}, {"test": _("test2")}]}}
    assert serializer.serialize_object(test) == '{"title_l10n": "test"}'
    assert (
        serializer.serialize_object_list(list_test)
        == '{"hits": {"hits": [{"title_l10n": "test1"}, {"title_l10n": "test2"}]}}'
    )


def test_marshmallow_json_serializer_with_context():
    serializer = MarshmallowSerializer(
        format_serializer_cls=JSONSerializer,
        object_schema_cls=UITestSchema,
        list_schema_cls=BaseListSchema,
        schema_context={"object_key": "ui"},
    )
    test = {"test": _("test")}
    list_test = {"hits": {"hits": [{"test": _("test1")}, {"test": _("test2")}]}}
    assert (
        serializer.serialize_object(test)
        == '{"test": "test", "ui": {"title_l10n": "test"}}'
    )
    assert (
        serializer.serialize_object_list(list_test)
        == '{"hits": {"hits": [{"test": "test1", "ui": {"title_l10n": "test1"}}, {"test": "test2", "ui": {"title_l10n": "test2"}}]}}'
    )


def test_marshmallow_csv_serializer_without_context():
    serializer = MarshmallowSerializer(
        format_serializer_cls=CSVSerializer,
        object_schema_cls=UITestSchema,
        list_schema_cls=BaseListSchema,
    )
    test = {"test": _("test")}
    list_test = {"hits": {"hits": [{"test": _("test1")}, {"test": _("test2")}]}}
    assert serializer.serialize_object(test) == "\r\n".join(["title_l10n", "test", ""])
    assert serializer.serialize_object_list(list_test) == "\r\n".join(
        ["title_l10n", "test1", "test2", ""]
    )


def test_marshmallow_csv_serializer_with_context():
    serializer = MarshmallowSerializer(
        format_serializer_cls=CSVSerializer,
        object_schema_cls=UITestSchema,
        list_schema_cls=BaseListSchema,
        schema_context={"object_key": "ui"},
    )
    test = {"test": _("test")}
    list_test = {"hits": {"hits": [{"test": _("test1")}, {"test": _("test2")}]}}
    assert serializer.serialize_object(test) == "\r\n".join(
        ["test,ui_title_l10n", "test,test", ""]
    )
    assert serializer.serialize_object_list(list_test) == "\r\n".join(
        ["test,ui_title_l10n", "test1,test1", "test2,test2", ""]
    )
