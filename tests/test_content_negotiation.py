# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
# Copyright (C) 2020 Northwestern University.
#
# Flask-Resources is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

from werkzeug.datastructures import MIMEAccept
from werkzeug.http import parse_accept_header

from flask_resources.content_negotiation import ContentNegotiator


# Test content negotiation by Accept header
# NOTE: By scoping down we remove the need to check for HTTP method
def test_choose_provided_and_accepted_mimetype():
    # Should choose mimetype that is accepted by client and served by server
    server_mimetypes = ["application/json", "application/marcxml+xml"]
    client_mimetypes = parse_accept_header(
        "text/plain,application/json,*/*", MIMEAccept
    )

    assert "application/json" == ContentNegotiator.match_by_accept(
        server_mimetypes, client_mimetypes
    )

    client_mimetypes = parse_accept_header(
        "text/plain,application/marcxml+xml,*/*", MIMEAccept
    )

    assert "application/marcxml+xml" == ContentNegotiator.match_by_accept(
        server_mimetypes, client_mimetypes
    )


def test_favour_specificity_over_quality():
    # favour more specific but lower quality mimetype over
    # less specific (e.g. wildcard) but higher quality
    server_mimetypes = ["application/json", "application/marcxml+xml"]
    client_mimetypes = parse_accept_header(
        "text/plain, application/json;q=0.5, */*", MIMEAccept
    )

    assert "application/json" == ContentNegotiator.match_by_accept(
        server_mimetypes, client_mimetypes
    )


def test_favour_quality_over_same_specificity():
    server_mimetypes = ["application/json", "application/marcxml+xml"]
    client_mimetypes = parse_accept_header(
        "application/json;q=0.5, application/marcxml+xml", MIMEAccept
    )

    assert "application/marcxml+xml" == ContentNegotiator.match_by_accept(
        server_mimetypes, client_mimetypes
    )

    client_mimetypes = parse_accept_header(
        "application/marcxml+xml;q=0.4, application/json;q=0.6", MIMEAccept
    )

    assert "application/json" == ContentNegotiator.match_by_accept(
        server_mimetypes, client_mimetypes
    )


def test_choose_default_if_no_match_and_wildcard_accepted():
    # choose default if no match and client accepts wildcard
    server_mimetypes = ["application/json", "application/marcxml+xml"]
    client_mimetypes = parse_accept_header("text/plain,*/*", MIMEAccept)

    assert "application/json" == ContentNegotiator.match_by_accept(
        server_mimetypes, client_mimetypes, default="application/json"
    )


def test_choose_none_if_no_match_and_wildcard_not_accepted():
    server_mimetypes = ["application/json", "application/marcxml+xml"]
    client_mimetypes = parse_accept_header("text/plain", MIMEAccept)

    mime_type = ContentNegotiator.match_by_accept(
        server_mimetypes, client_mimetypes, default="application/json"
    )

    assert mime_type is None


def test_choose_default_if_nothing_accepted():
    server_mimetypes = ["application/json", "application/marcxml+xml"]
    client_mimetypes = parse_accept_header("", MIMEAccept)

    assert "application/json" == ContentNegotiator.match_by_accept(
        server_mimetypes, client_mimetypes, default="application/json"
    )


# Test content negotiation by URL argument
# NOTE: By scoping down we remove the need to check for HTTP method
def test_choose_query_mimetype():
    formats_map = {
        "json": "application/json",
        "marcxml": "application/marcxml+xml",
    }
    fmt = "marcxml"  # this is the query

    assert "application/marcxml+xml" == ContentNegotiator.match_by_format(
        formats_map, fmt
    )

    fmt = "json"

    assert "application/json" == ContentNegotiator.match_by_format(formats_map, fmt)

    fmt = "foo"

    mime_type = ContentNegotiator.match_by_format(formats_map, fmt)

    assert mime_type is None


# Test top-level ContentNegotiator.match
def test_favour_query_mimetype_over_header_mimetype():
    server_mimetypes = ["application/json", "application/marcxml+xml"]
    client_mimetypes = parse_accept_header("application/json", MIMEAccept)
    formats_map = {
        "json": "application/json",
        "marcxml": "application/marcxml+xml",
    }
    fmt = "marcxml"

    assert "application/marcxml+xml" == ContentNegotiator.match(
        server_mimetypes, client_mimetypes, formats_map, fmt
    )

    client_mimetypes = parse_accept_header("application/marcxml+xml", MIMEAccept)
    fmt = "json"

    assert "application/json" == ContentNegotiator.match(
        server_mimetypes, client_mimetypes, formats_map, fmt
    )


def test_favour_header_mimetype_if_no_query_mimetype():
    server_mimetypes = ["application/json", "application/marcxml+xml"]
    client_mimetypes = parse_accept_header("application/json", MIMEAccept)
    formats_map = {
        "json": "application/json",
        "marcxml": "application/marcxml+xml",
    }
    fmt = None

    assert "application/json" == ContentNegotiator.match(
        server_mimetypes, client_mimetypes, formats_map, fmt
    )

    formats_map = {}
    fmt = "marcxml"

    assert "application/json" == ContentNegotiator.match(
        server_mimetypes, client_mimetypes, formats_map, fmt
    )


def test_choose_default_if_no_query_and_no_header():
    server_mimetypes = ["application/json", "application/marcxml+xml"]
    client_mimetypes = parse_accept_header("", MIMEAccept)
    formats_map = {
        "json": "application/json",
        "marcxml": "application/marcxml+xml",
    }
    fmt = None

    assert "application/json" == ContentNegotiator.match(
        server_mimetypes, client_mimetypes, formats_map, fmt, default="application/json"
    )
