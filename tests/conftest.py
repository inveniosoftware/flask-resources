# SPDX-FileCopyrightText: 2020 CERN.
# SPDX-License-Identifier: MIT

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
