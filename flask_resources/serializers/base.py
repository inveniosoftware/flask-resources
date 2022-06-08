# -*- coding: utf-8 -*-
#
# Copyright (C) 2020-2021 CERN.
# Copyright (C) 2020-2021 Northwestern University.
#
# Flask-Resources is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Serializers required interfaces."""
from copy import deepcopy


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


class MarshmallowSerializer(SerializerMixin):
    """Marshmallow serializer that serializes an obj into defined schema.

    :param format_serializer_cls: Serializer in charge of converting the data object into
        the desired format.
    :param object_schema_cls: Marshmallow Schema of the object.
    :param list_schema_cls: Marshmallow Schema of the object list.
    :param schema_context: Context of the Marshmallow Schema.
    """

    def __init__(
        self,
        format_serializer_cls,
        object_schema_cls,
        list_schema_cls=None,
        schema_context={},
        **serializer_options
    ):
        """Initialize the serializer."""
        self.schema_context = schema_context
        self.object_schema_cls = object_schema_cls
        self.list_schema_cls = list_schema_cls
        self.format_serializer_cls = format_serializer_cls(**serializer_options)

    def dump_obj(self, obj):
        """Dump the object using object schema class."""
        ser_obj = deepcopy(obj)
        return self.object_schema_cls(context=self.schema_context).dump(ser_obj)

    def dump_list(self, obj_list):
        """Dump the list of objects."""
        ctx = {
            "object_schema_cls": self.object_schema_cls,
        }
        ctx.update(self.schema_context)

        if self.list_schema_cls is None:
            return self.object_schema_cls(context=self.schema_context).dump(
                obj_list, many=True
            )

        return self.list_schema_cls(context=ctx).dump(obj_list)

    def serialize_object(self, obj):
        """Dump the object using the serializer."""
        return self.format_serializer_cls.serialize_object(self.dump_obj(obj))

    def serialize_object_list(self, obj_list):
        """Dump the object list using the serializer."""
        return self.format_serializer_cls.serialize_object_list(
            self.dump_list(obj_list)
        )
