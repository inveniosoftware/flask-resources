# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
# Copyright (C) 2020 Northwestern University.
#
# Flask--Resources is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

from werkzeug.datastructures import MIMEAccept
from werkzeug.http import parse_accept_header

from flask_resources.content_negotiation import ContentNegotiator


# Test content negotiation by Accept header
# NOTE: By scoping down we remove the need to check for HTTP method
def test_choose_provided_and_accepted_mimetype():
    # Should choose mimetype that is accepted by client and served by server
    server_mimetypes = ['application/json', 'application/marcxml+xml']
    client_mimetypes = parse_accept_header(
        'text/plain,application/json,*/*',
        MIMEAccept
    )

    mime_type = ContentNegotiator.match_by_accept(
        server_mimetypes, client_mimetypes
    )

    assert 'application/json' == mime_type

    client_mimetypes = parse_accept_header(
        'text/plain,application/marcxml+xml,*/*',
        MIMEAccept
    )

    mime_type = ContentNegotiator.match_by_accept(
        server_mimetypes, client_mimetypes
    )

    assert 'application/marcxml+xml' == mime_type


def test_favour_specificity_over_quality():
    # favour more specific but lower quality mimetype over
    # less specific (e.g. wildcard) but higher quality
    server_mimetypes = ['application/json', 'application/marcxml+xml']
    client_mimetypes = parse_accept_header(
        'text/plain, application/json;q=0.5, */*',
        MIMEAccept
    )

    mime_type = ContentNegotiator.match_by_accept(
        server_mimetypes, client_mimetypes
    )

    assert 'application/json' == mime_type


def test_favour_quality_over_same_specificity():
    server_mimetypes = ['application/json', 'application/marcxml+xml']
    client_mimetypes = parse_accept_header(
        'application/json;q=0.5, application/marcxml+xml',
        MIMEAccept
    )

    mime_type = ContentNegotiator.match_by_accept(
        server_mimetypes, client_mimetypes
    )

    assert 'application/marcxml+xml' == mime_type

    client_mimetypes = parse_accept_header(
        'application/marcxml+xml;q=0.4, application/json;q=0.6',
        MIMEAccept
    )

    mime_type = ContentNegotiator.match_by_accept(
        server_mimetypes, client_mimetypes
    )

    assert 'application/json' == mime_type


def test_choose_default_if_no_match_and_wildcard_accepted():
    # choose default if no match and client accepts wildcard
    server_mimetypes = ['application/json', 'application/marcxml+xml']
    client_mimetypes = parse_accept_header(
        'text/plain,*/*',
        MIMEAccept
    )

    mime_type = ContentNegotiator.match_by_accept(
        server_mimetypes, client_mimetypes, default='application/json'
    )

    assert 'application/json' == mime_type


def test_choose_none_if_no_match_and_wildcard_not_accepted():
    server_mimetypes = ['application/json', 'application/marcxml+xml']
    client_mimetypes = parse_accept_header(
        'text/plain',
        MIMEAccept
    )

    mime_type = ContentNegotiator.match_by_accept(
        server_mimetypes, client_mimetypes, default='application/json'
    )

    assert mime_type is None


def test_choose_default_if_nothing_accepted():
    server_mimetypes = ['application/json', 'application/marcxml+xml']
    client_mimetypes = parse_accept_header(
        '',
        MIMEAccept
    )

    mime_type = ContentNegotiator.match_by_accept(
        server_mimetypes, client_mimetypes, default='application/json'
    )

    assert 'application/json' == mime_type


# Test content negotiation by URL argument
# NOTE: By scoping down we remove the need to check for HTTP method
def test_choose_query_mimetype():
    formats_map = {
        'json': 'application/json',
        'marcxml': 'application/marcxml+xml',
    }
    fmt = 'marcxml'

    mime_type = ContentNegotiator.match_by_format(formats_map, fmt)

    assert 'application/marcxml+xml' == mime_type

    fmt = 'json'

    mime_type = ContentNegotiator.match_by_format(formats_map, fmt)

    assert 'application/json' == mime_type

    fmt = 'foo'

    mime_type = ContentNegotiator.match_by_format(formats_map, fmt)

    assert mime_type is None


# TODO: Fill tests for top-level match
def test_favour_query_over_header():
    # (urlencode({arg_name: 'marcxml'}), 'application/json', 'xml-get'),
    # (urlencode({arg_name: 'json'}), 'application/marcxml+xml',
    pass


def test_favour_header_if_no_query():
    # Should serialize to json
    # (urlencode({}), 'application/json', 'json-get'),
    pass


def test_choose_default_if_no_query_and_no_header():
    # Should serialize to json
    # (urlencode({}), 'application/json', 'json-get'),
    pass
