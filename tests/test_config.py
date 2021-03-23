# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
# Copyright (C) 2020 Northwestern University.
#
# Flask-Resources is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

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
