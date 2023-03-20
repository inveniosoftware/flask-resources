# -*- coding: utf-8 -*-
#
# Copyright (C) 2020-2023 CERN.
# Copyright (C) 2020-2021 Northwestern University.
#
# Flask-Resources is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Serializers required interfaces."""
from abc import ABC, abstractmethod
from copy import deepcopy


class BaseSerializer(ABC):
    """Serializer Interface."""

    @abstractmethod
    def serialize_object(self, obj):
        """Serialize a single object according to the response ctx.

        The object type must implement ``SerializableMixin``.
        """
        pass

    def serialize_object_list(self, obj_list):
        """Serialize a list of objects according to the response ctx.

        Each object type of the list should implement ``SerializableMixin``.
        """
        pass


class MarshmallowSerializer(BaseSerializer):
    """Marshmallow serializer that serializes an obj into defined schema.

    :param format_serializer_cls: Serializer in charge of converting the data object into
        the desired format.
    :param object_schema_cls: Marshmallow Schema of the object.
    :param list_schema_cls: Marshmallow Schema of the object list.
    :param schema_context: Context of the Marshmallow Schema.
    :param schema_kwargs: Additional arguments to be passed to marshmallow schema.
    """

    def __init__(
        self,
        format_serializer_cls,
        object_schema_cls,
        list_schema_cls=None,
        schema_context=None,
        schema_kwargs=None,
        **serializer_options
    ):
        """Initialize the serializer."""
        self.schema_context = schema_context or {}
        schema_kwargs = schema_kwargs or {}

        self.format_serializer = format_serializer_cls(**serializer_options)
        self.object_schema = object_schema_cls(context=schema_context, **schema_kwargs)
        if list_schema_cls:
            self.list_schema = list_schema_cls(
                context={
                    "object_schema_cls": self.object_schema.__class__,
                    **self.schema_context,
                }
            )
        else:
            self.list_schema = None

    def dump_obj(self, obj):
        """Dump the object using object schema class."""
        return self.object_schema.dump(obj)

    def dump_list(self, obj_list):
        """Dump the list of objects."""
        if not self.list_schema:
            return self.object_schema.dump(obj_list, many=True)

        return self.list_schema.dump(obj_list)

    def serialize_object(self, obj):
        """Dump the object using the serializer."""
        return self.format_serializer.serialize_object(self.dump_obj(obj))

    def serialize_object_list(self, obj_list):
        """Dump the object list using the serializer."""
        return self.format_serializer.serialize_object_list(self.dump_list(obj_list))
