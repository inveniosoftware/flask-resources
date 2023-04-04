# -*- coding: utf-8 -*-
#
# Copyright (C) 2020-2023 CERN.
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


# this class is not used since there is no MarshmallowDeserializer/Deformatter/Loader
class LoaderMixin:
    """Abstract class that defines an interface for pre_load and post_load methods.

    This allows the extension of records deserialization.
    """

    def post_load(data, **kwargs):
        """Hook called after the marshmallow deserialization of the record.

        :param data: The loaded record data, already deserialized.
        :param kwargs: Additional keyword arguments.
        :returns: The deserialized record data.
        """
        return data

    def pre_load(data, **kwargs):
        """Hook called before the marshmallow deserialization of the record.

        :param data: The record data before being deserialized.
        :param kwargs: Additional keyword arguments.
        :returns: The record data.
        """
        return data
