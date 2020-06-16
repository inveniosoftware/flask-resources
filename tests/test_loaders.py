# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
#
# Flask--Resources is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""Loaders test module."""

import json

from flask import request

from flask_resources.loaders import JSONLoader, JSONPatchLoader, LoaderMixin


class CustomLoader(LoaderMixin):
    """Custom loader implementation."""

    def load_request(self, *args, **kwargs):
        """Load the request."""
        return request.get_data()


def test_custom_loader(mocker):
    """Test custom loader."""
    request_body = {"field_one": "value", "field_two": "some other value"}

    def get_data():
        return str(request_body)

    request_mock = mocker.patch("tests.test_loaders.request")
    request_mock.get_data = get_data

    loader = CustomLoader()
    assert loader.load_request() == str(request_body)


def test_json_loader(mocker):
    """Test JSON loader."""
    request_body = {"field_one": "value", "field_two": "some other value"}

    def get_json():
        return json.dumps(request_body)

    request_mock = mocker.patch("flask_resources.loaders.json.request")
    request_mock.get_json = get_json

    loader = JSONLoader()
    assert loader.load_request() == json.dumps(request_body)


def test_json_patch_loader(mocker):
    """Test JSON loader."""
    request_body = {"op": "replace", "path": "/field_one", "value": "something patched"}

    def get_json(force=None):
        return json.dumps(request_body)

    request_mock = mocker.patch("flask_resources.loaders.json.request")
    request_mock.get_json = get_json

    loader = JSONPatchLoader()
    assert loader.load_request() == json.dumps(request_body)
