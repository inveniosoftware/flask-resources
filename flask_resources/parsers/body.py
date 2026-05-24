# SPDX-FileCopyrightText: 2020-2021 CERN.
# SPDX-FileCopyrightText: 2020-2021 Northwestern University.
# SPDX-License-Identifier: MIT

"""Request body parsers module."""

from flask import request


class RequestBodyParser:
    """Parse the request body."""

    def __init__(self, deserializer):
        """Constructor."""
        self.deserializer = deserializer

    def parse(self):
        """Parse the request body."""
        return self.deserializer.deserialize(request.data)
