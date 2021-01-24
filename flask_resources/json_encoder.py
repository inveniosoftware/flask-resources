# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
# Copyright (C) 2020 Northwestern University.
#
# Flask-Resources is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Custom JSON encoder."""


from flask.json import JSONEncoder
from speaklater import is_lazy_string


class CustomJSONEncoder(JSONEncoder):
    """JSONEncoder for our custom needs.

    - Knows to force translate lazy translation strings
    """

    def default(self, obj):
        """Override parent's default."""
        if is_lazy_string(obj):
            return str(obj)
        return super().default(obj)
