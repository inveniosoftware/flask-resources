# -*- coding: utf-8 -*-
#
# Copyright (C) 2020-2021 CERN.
# Copyright (C) 2020-2021 Northwestern University.
#
# Flask-Resources is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Content negotiation API."""

from functools import wraps

from flask import request
from werkzeug.datastructures import MIMEAccept

from .config import resolve_from_conf
from .context import resource_requestctx
from .errors import MIMETypeNotAccepted


class ContentNegotiator(object):
    """Content negotiation API.

    Implements a procedure for selecting a mimetype best matching what the
    client is requesting.
    """

    @classmethod
    def match(cls, mimetypes, accept_mimetypes, formats_map, fmt, default=None):
        """Select the MIME type which best matches the client request.

        :param mimetypes: Iterable of available MIME types.
        :param accept_mimetypes: The client's "Accept" header as MIMEAccept
            object.
        :param formats_map: Map of format values to MIME type.
        :param format: The client's selected format.
        :param default: Default MIMEtype if a wildcard was received.
        """
        return cls.match_by_format(formats_map, fmt) or cls.match_by_accept(
            mimetypes, accept_mimetypes, default=default
        )

    @classmethod
    def match_by_accept(cls, mimetypes, accept_mimetypes, default=None):
        """Select the MIME type which best matches Accept header.

        NOTE: Our match policy differs from Werkzeug's best_match policy:
              If the client accepts a specific mimetype and wildcards, and
              the server serves that specific mimetype, then favour
              that mimetype no matter its quality over the wildcard.
              This is as opposed to Werkzeug which only cares about quality.

        :param mimetypes: Iterable of available MIME types.
        :param accept_mimetypes: The client's "Accept" header as MIMEAccept
            object.
        :param default: Default MIMEtype if wildcard received.
        """
        assert isinstance(accept_mimetypes, MIMEAccept)
        assert "*/*" not in mimetypes

        # NOTE: accept_mimetypes is already sorted in descending quality order
        for client_mimetype, quality in accept_mimetypes:
            if client_mimetype in mimetypes:
                return client_mimetype

        # if here, then no match at all
        # WARNING: '*/*' in MIMEAccept object always evaluates to True
        # WARNING: MIMEAccept.find('*/*') always evaluates to 0
        # So we have to do the following
        accepted_values = list(accept_mimetypes.values())
        if "*/*" in accepted_values or not accepted_values:
            return default

        return None

    @classmethod
    def match_by_format(cls, formats_map, fmt):
        """Select the MIME type based on a query parameters."""
        return formats_map.get(fmt)


def with_content_negotiation(
    response_handlers=None,
    default_accept_mimetype=None,
):
    """Decorator to perform content negotiation.

    The result of the content negotiation is stored in the resources request
    context.
    """

    def decorator(f):
        @wraps(f)
        def inner_content_negotiation(*args, **kwargs):
            # Check Accept header i.e. can we even respond to the request in a common
            # mimetype?
            handlers = resolve_from_conf(response_handlers, resource_requestctx.config)
            default_mimetype = resolve_from_conf(
                default_accept_mimetype, resource_requestctx.config
            )

            accept_mimetype = ContentNegotiator.match(
                handlers.keys(),
                request.accept_mimetypes,
                {},  # TODO: Rely on config to populate this formats_map
                request.args.get("format", None),
                default_mimetype,
            )

            if not accept_mimetype:
                raise MIMETypeNotAccepted(allowed_mimetypes=handlers.keys())

            resource_requestctx.accept_mimetype = accept_mimetype
            resource_requestctx.response_handler = handlers[accept_mimetype]

            return f(*args, **kwargs)

        return inner_content_negotiation

    return decorator
