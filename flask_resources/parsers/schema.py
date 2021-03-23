# -*- coding: utf-8 -*-
#
# Copyright (C) 2020-2021 CERN.
# Copyright (C) 2020-2021 Northwestern University.
#
# Flask-Resources is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Schema that's able to handle loading data from MultiDicts."""

import marshmallow as ma
from werkzeug.datastructures import MultiDict


class MultiDictSchema(ma.Schema):
    """MultiDict aware schema used for loading e.g. request.args."""

    class Meta:
        """Throw away unknown values."""

        unknown = ma.EXCLUDE

    LIST_TYPES = [
        ma.fields.List,
    ]

    @classmethod
    def is_list_field(cls, field):
        """Method used to determine if a field is a list type field.

        This is used to unpack the MultiDict into a normal dictionary.
        """
        return any((isinstance(field, t) for t in cls.LIST_TYPES))

    @ma.pre_load
    def flatten_multidict(self, data, **kwargs):
        """Flatten a MultiDict into a normal dictionary."""
        if not isinstance(data, MultiDict):
            return data
        data = data.to_dict(flat=False)

        for name, field in self.fields.items():
            if name in data and not self.is_list_field(field):
                data[name] = data[name][0]
        return data
