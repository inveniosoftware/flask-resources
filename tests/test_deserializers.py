# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
# Copyright (C) 2020 Northwestern University.
#
# Flask-Resources is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""Test deserialization."""

import json

from flask_resources import JSONDeserializer


def test_json_deserializer():
    data = {"a": "test"}
    assert JSONDeserializer().deserialize(json.dumps(data)) == data

    data = {}
    assert JSONDeserializer().deserialize(json.dumps(data)) == {}

    data = None
    assert JSONDeserializer().deserialize(json.dumps(data)) is None
