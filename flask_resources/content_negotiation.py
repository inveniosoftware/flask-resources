# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
#
# Flask-Resources is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Content negotiation API."""

from functools import wraps

from werkzeug.datastructures import MIMEAccept

from .context import resource_requestctx
from .errors import UnsupportedMimetypeError


class ContentNegotiator(object):
    """Content negotiation API.

    Implements a procedure for selecting a mimetype best matching what the
    client is requesting.
    """

    @classmethod
    def match(cls, mimetypes, accept_mimetypes, formats_map, format, default=None):
        """Select the MIME type which best matches the client request.

        :param mimetypes: List/set of available MIME types.
        :param accept_mimetypes: The clients "Accept" header as MIMEAccept
            object.
        :param formats_map: Map of format values to MIME type.
        :param format: The client's selected format.
        :param default: Default MIMEtype if a wildcard was received.
        """
        return cls.match_by_format(formats_map, format) or cls.match_by_accept(
            mimetypes, accept_mimetypes, default=default
        )

    @classmethod
    def match_by_accept(cls, mimetypes, accept_mimetypes, default=None):
        """Select the MIME type which best matches Accept header."""
        # Bail out fast if no accept headers were given.
        if len(accept_mimetypes) == 0:
            return default

        # Determine best match based on quality.
        best_quality = -1
        best = None
        has_wildcard = False
        for client_accept, quality in accept_mimetypes:
            if quality <= best_quality:
                continue
            if client_accept == "*/*":
                has_wildcard = True
            for m in mimetypes:
                if m in ["*/*", client_accept] and quality > 0:
                    best_quality = quality
                    best = m

        # If no match found, but wildcard exists, them use default media
        # type.
        if best is None and has_wildcard:
            best = default

        return best

    @classmethod
    def match_by_format(cls, formats_map, format):
        """Select the MIME type based on a query parameters."""
        if format is None:
            return None

        try:
            return formats_map[format]
        except KeyError:
            return None


def content_negotiation(f):
    """Decorator to perform content negotiation."""

    @wraps(f)
    def inner(self, *args, **kwargs):
        # resource_requestctx.payload_mimetype = ContentNegotiator.match(
        #     self.item_loaders.keys(),
        #     request.content_type,
        #     {},  # self.formats,
        #     request.args.get("format", None),
        #     None,  # self.default_mimetype,
        # )

        # FIXME: content negotiation
        payload_mimetype = "application/json"  # Content-Type
        accept_mimetype = "application/json"

        # Check if content-type can be treated otherwise, fail fast
        # Serialization is checked per function due to lack of
        # knowledge at this point
        allowed_mimetypes = self.request_loaders.keys()
        if payload_mimetype not in allowed_mimetypes:
            raise UnsupportedMimetypeError(
                header="Content-Type",
                received_mimetype=payload_mimetype,
                allowed_mimetypes=allowed_mimetypes,
            )

        allowed_mimetypes = self.response_handlers.keys()
        if accept_mimetype not in allowed_mimetypes:
            raise UnsupportedMimetypeError(
                header="Accept",
                received_mimetype=accept_mimetype,
                allowed_mimetypes=allowed_mimetypes,
            )

        resource_requestctx.payload_mimetype = payload_mimetype
        resource_requestctx.accept_mimetype = accept_mimetype

        return f(self, *args, **kwargs)

    return inner
