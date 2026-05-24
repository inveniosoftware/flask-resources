# SPDX-FileCopyrightText: 2020 CERN.
# SPDX-FileCopyrightText: 2020 Northwestern University.
# SPDX-License-Identifier: MIT

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
