# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
# Copyright (C) 2020 Northwestern University.
#
# Flask-Resources is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Deserializers required interfaces."""


class DeserializerMixin:
    """Deserializer Interface."""

    def deserialize_data(self, data, *args, **kwargs):
        """Deserializes an object."""
        raise NotImplementedError()
