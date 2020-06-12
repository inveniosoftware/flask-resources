# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
#
# Flask-Resources is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Content negotiation API."""

from werkzeug.datastructures import MIMEAccept


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

        NOTE: Match policy differs from Werkzeug's best_match policy.
        - If client accepts specific and wildcard, and server serves specific,
          then favour specific no matter the client quality.

        TODO: Choose the explicit policy for this "best match".
        Meanwhile, the policy implemented below is:

            Select the highest quality (accepted) + provided mimetype.
            If no match,
                but accept wildcard, return default
                otherwise if provide wildcard, return wildcard
                else: return None

        This is probably not an ideal policy.

        :param mimetypes: Iterable of available MIME types.
        :param accept_mimetypes: The client's "Accept" header as MIMEAccept
            object.
        :param mimetypes: Default MIMEtype if wildcard received.
        """
        assert isinstance(accept_mimetypes, MIMEAccept)

        # NOTE: accept_mimetypes is already sorted in descending quality order
        for client_mimetype, quality in accept_mimetypes:
            if client_mimetype in mimetypes:
                return client_mimetype

        # if here, then no match at all
        # WARNING: '*/*' in MIMEAccept object always evaluates to True
        # WARNING: MIMEAccept.find('*/*') always evaluates to 0
        # So we have to do the following
        accepted_values = list(accept_mimetypes.values())
        if '*/*' in accepted_values or not accepted_values:
            return default

        # TODO: What happens if server provides */* ? Is that possible?

        return None

    @classmethod
    def match_by_format(cls, formats_map, fmt):
        """Select the MIME type based on a query parameters."""
        return formats_map.get(fmt)
