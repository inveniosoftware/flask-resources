# SPDX-FileCopyrightText: 2020-2021 CERN.
# SPDX-FileCopyrightText: 2020-2021 Northwestern University.
# SPDX-License-Identifier: MIT

"""JSON Deserializer."""

import json

from .base import DeserializerMixin


class JSONDeserializer(DeserializerMixin):
    """JSON Deserializer."""

    def deserialize(self, data):
        """Deserializes JSON into a Python dictionary."""
        return json.loads(data) if data else None
