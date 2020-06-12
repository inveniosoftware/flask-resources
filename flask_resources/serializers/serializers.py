# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
#
# Flask-Resources is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Serializers and required interfaces."""


class SerializableMixin:
    """Serializable Interface.

    Objects that will be serialized must implement it.
    """

    @property
    def object():
        """Returns the object itself."""
        raise NotImplementedError()

    @property
    def id():
        """Returns the object id."""
        raise NotImplementedError()

    @property
    def version():
        """Returns the object version or revision."""
        raise NotImplementedError()

    @property
    def last_modified():
        """Returns the date of the last modification."""
        raise NotImplementedError()


class SerializerMixin:
    """Serializer Interface."""

    def serialize_object(self, object, response_ctx, *args, **kwargs):
        """Serialize a single object according to the response ctx.

        The object type must implement ``SerializableMixin``.
        """
        raise NotImplementedError()

    def serialize_object_list(self, object_list, response_ctx, *args, **kwargs):
        """Serialize a list of objects according to the response ctx.

        Each object type of the list should implement ``SerializableMixin``.
        """
        raise NotImplementedError()

    def serialize_error(self, error, response_ctx, *args, **kwargs):
        """Serialize an error reponse according to the response ctx."""
        raise NotImplementedError()
