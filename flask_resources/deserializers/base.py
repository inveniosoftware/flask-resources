# -*- coding: utf-8 -*-
#
# Copyright (C) 2020-2021 CERN.
# Copyright (C) 2020-2021 Northwestern University.
#
# Flask-Resources is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Deserializers required interfaces."""


class DeserializerMixin:
    """Deserializer Interface."""

    def deserialize(self, data):
        """Deserializes the data into an object."""
        raise NotImplementedError()
