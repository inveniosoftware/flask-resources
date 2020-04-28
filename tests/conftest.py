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
def create_app(instance_path):
    """Application factory fixture."""

    def app(*args, **kwargs):
        """Create app."""
        app_ = Flask(__name__)

        return app_

    return app
