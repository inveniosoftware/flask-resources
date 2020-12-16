# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
# Copyright (C) 2020 Northwestern University.
#
# Flask-Resources is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""Test deserialization."""

from speaklater import make_lazy_string

from flask_resources.serializers import JSONSerializer


def _(s):
    return make_lazy_string(lambda: s)


def test_lazy_strings_are_deserialized():
    serializer = JSONSerializer()
    lazy = {"key": _("Lazy")}
    list_lazy = [{"key": _("Lazy1")}, {"key": _("Lazy2")}]

    assert '{"key": "Lazy"}' == serializer.serialize_object(lazy)
    assert '[{"key": "Lazy1"}, {"key": "Lazy2"}]' == serializer.serialize_object_list(
        list_lazy
    )
