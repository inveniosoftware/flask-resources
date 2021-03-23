# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
#
# Flask--Resources is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""Pytest configuration.

See https://pytest-invenio.readthedocs.io/ for documentation on which test
fixtures are available.
"""

import pytest
from flask import Flask


@pytest.fixture(scope="module")
def app(resource):
    """Doc example app."""
    app = Flask("test")
    app.register_blueprint(resource.as_blueprint())
    return app
