# -*- coding: utf-8 -*-
#
# Copyright (C) 2020-2023 CERN.
# Copyright (C) 2020-2021 Northwestern University.
#
# Flask-Resources is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Serializers required interfaces."""

from abc import ABC, abstractmethod

from marshmallow import Schema, post_dump, pre_dump


class BaseSerializer(ABC):
    """Serializer Interface."""

    @abstractmethod
    def serialize_object(self, obj):
        """Serialize a single object according to the response ctx."""
        pass

    def serialize_object_list(self, obj_list):
        """Serialize a list of objects according to the response ctx."""
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
                    "object_schema_cls": object_schema_cls,
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


class DumperMixin:
    """Abstract class that defines an interface for pre_dump and post_dump methods.

    It allows to extend records serialization.
    """

    def post_dump(self, data, original=None, **kwargs):
        """Hook called after the marshmallow serialization of the record.

        :param data: The dumped record data.
        :param original: The original record data.
        :param kwargs: Additional keyword arguments.
        :returns: The serialized record data.
        """
        return data

    def pre_dump(self, data, original=None, **kwargs):
        """
        Hook called before the marshmallow serialization of the record.

        :param data: The record data to dump.
        :param original: The original record data.
        :param kwargs: Additional keyword arguments.
        :returns: The data to dump.
        """
        return data


# FIXME: This should be moved to the base transformer class on
# https://github.com/inveniosoftware/flask-resources/issues/117


class BaseSerializerSchema(Schema):
    """Enables the extension of Marshmallow schemas serialization."""

    def __init__(self, dumpers=None, **kwargs):
        """Constructor."""
        super().__init__(**kwargs)
        self.dumpers = dumpers or []

    @post_dump(pass_original=True)
    def post_dump_pipeline(self, data, original, many, **kwargs):
        """Applies a sequence of post-dump steps to the serialized data.

        :param data: The result of serialization.
        :param original: The original object that was serialized.
        :param many: Whether the serialization was done on a collection of objects.

        :returns: The result of the pipeline processing on the serialized data.
        """
        for dumper in self.dumpers:
            # Data is assumed to be modified and returned by the dumper
            data = dumper.post_dump(data, original)
        return data

    @pre_dump
    def pre_dump_pipeline(self, data, many, **kwargs):
        """Applies a sequence of pre-dump steps to the input data.

        :param data: The result of serialization.
        :param many: Whether the serialization was done on a collection of objects.

        :returns: The result of the pipeline processing on the serialized data.
        """
        for dumper in self.dumpers:
            # Data is assumed to be modified and returned by the dumper
            data = dumper.pre_dump(data)
        return data
