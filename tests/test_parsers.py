# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
#
# Flask--Resources is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""Parses test module."""

import pytest
from marshmallow.exceptions import ValidationError
from werkzeug.exceptions import HTTPException

from flask_resources.parsers import (
    create_request_parser,
    item_request_parser,
    search_request_parser,
)


def assert_validation_error(error, message=None):
    """Validates that the error was risen from a ValidationError.

    Optionally checks the ValidationError message for a specific string.
    """
    # Check that is a validation error
    assert type(error.value.exc) == ValidationError
    # The abort error is a 422 UnprocessableEntity
    assert error.value.code == 422

    if message:
        assert message in str(error.value.exc.messages)


#
# Search Request Parser
#


def test_search_request_parser_default_values(app):
    """Test default search request parser."""
    with app.test_request_context(
        "/", method="get", content_type="application/json",
    ):
        parsed_args = search_request_parser.parse()

        assert parsed_args.get("size") == 10
        assert parsed_args.get("page") == 1
        assert parsed_args.get("q") == ""
        # pagination values themselves are tested independently
        assert parsed_args.get("pagination") is not None


def test_search_request_parser_custom_values(app):
    """Test default search request parser."""
    with app.test_request_context(
        "/?size=5&page=10&q=test", method="get", content_type="application/json",
    ):
        parsed_args = search_request_parser.parse()
        assert parsed_args.get("page") == 10
        assert parsed_args.get("size") == 5
        assert parsed_args.get("q") == "test"


def test_search_request_parser_validation_errors(app):
    """Test default search request parser."""
    with app.test_request_context(
        "/?page=-1", method="get", content_type="application/json",
    ):
        with pytest.raises(HTTPException) as error:
            parsed_args = search_request_parser.parse()
        assert_validation_error(error, "page")

    with app.test_request_context(
        "/?size=-1", method="get", content_type="application/json",
    ):
        with pytest.raises(HTTPException) as error:
            parsed_args = search_request_parser.parse()
        assert_validation_error(error, "size")

    with app.test_request_context(
        "/?from=-1", method="get", content_type="application/json",
    ):
        with pytest.raises(HTTPException) as error:
            parsed_args = search_request_parser.parse()
        assert_validation_error(error, "from")


#
# Item Request Parser
#


def test_item_request_parser(app):
    """Test default search request parser."""
    with app.test_request_context(
        "/?id=abcd", method="get", content_type="application/json",
    ):
        parsed_args = item_request_parser.parse()
        # validation corrected it, it has min=1
        assert parsed_args.get("id") == "abcd"


def test_item_request_parser_validation_error(app):
    """Test default item request parser."""
    with app.test_request_context(
        "/", method="get", content_type="application/json",
    ):
        # this test includes validation error becuase the field is required
        with pytest.raises(HTTPException) as error:
            parsed_args = item_request_parser.parse()
        assert_validation_error(error, "id")
