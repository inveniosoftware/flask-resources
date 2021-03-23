# -*- coding: utf-8 -*-
#
# Copyright (C) 2020-2021 CERN.
# Copyright (C) 2020-2021 Northwestern University.
#
# Flask-Resources is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Serializers required interfaces."""


class SerializerMixin:
    """Serializer Interface."""

    def serialize_object(self, obj):
        """Serialize a single object according to the response ctx.

        The object type must implement ``SerializableMixin``.
        """
        raise NotImplementedError()

    def serialize_object_list(self, obj_list):
        """Serialize a list of objects according to the response ctx.

        Each object type of the list should implement ``SerializableMixin``.
        """
        raise NotImplementedError()
