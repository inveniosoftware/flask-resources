# SPDX-FileCopyrightText: 2020 CERN.
# SPDX-FileCopyrightText: 2020 Northwestern University.
# SPDX-License-Identifier: MIT

"""Test config deferred values."""

import pytest

from flask_resources import from_conf
from flask_resources.config import resolve_from_conf


def test_from_conf():
    class Config:
        test = "val"

    assert resolve_from_conf(from_conf("test"), Config) == "val"
    assert resolve_from_conf("not-in-conf", Config) == "not-in-conf"
    pytest.raises(AttributeError, resolve_from_conf, from_conf("invalid"), Config)
