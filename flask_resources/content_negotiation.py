# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
#
# Flask-Resources is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Content negotiation API."""


class ContentNegotiator(object):
    """Content negotiation API.

    Implements a procedure for selecting a mimetype best matching what the
    client is requesting.
    """

    @classmethod
    def match(cls, mimetypes, accept_mimetypes, formats_map, format,
              default=None):
        """Select the MIME type which best matches the client request.

        :param mimetypes: Iterable of available MIME types.
        :param accept_mimetypes: The client's "Accept" header as MIMEAccept
            object.
        :param formats_map: Map of format values to MIME type.
        :param format: The client's selected format.
        :param default: Default MIMEtype if a wildcard was received.
        """
        return cls.match_by_format(formats_map, format) or \
            cls.match_by_accept(mimetypes, accept_mimetypes, default=default)

    @classmethod
    def match_by_accept(cls, mimetypes, accept_mimetypes, default=None):
        """Select the MIME type which best matches Accept header.

        TODO: Choose the explicit policy for this "best match".
        Meanwhile, the policy implemented below is:

            Select the highest quality (accepted) + provided mimetype.
            If no match,
                but accept wildcard, return default
                otherwise if provide wildcard, return wildcard
                else: return None

        This is probably not an ideal policy.
        """
        desc_client_mimetypes = sorted(accept_mimetypes, key=lambda m: -m[1])
        for client_mimetype, quality in desc_client_mimetypes:
            if client_mimetype in mimetypes:
                return client_mimetype

        # if here, then no match at all
        if '*/*' in accept_mimetypes:
            return default

        if '*/*' in mimetypes:
            return '*/*'  # NOTE: this is weird but that was the case before

        return default

    @classmethod
    def match_by_format(cls, formats_map, fmt):
        """Select the MIME type based on a query parameters."""
        return formats_map.get(fmt) if fmt else None
