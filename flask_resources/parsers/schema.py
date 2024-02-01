# -*- coding: utf-8 -*-
#
# Copyright (C) 2020-2024 CERN.
# Copyright (C) 2020-2021 Northwestern University.
#
# Flask-Resources is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Schema that's able to handle loading data from MultiDicts."""

from marshmallow import EXCLUDE, Schema, fields, missing, pre_load
from werkzeug.datastructures import MultiDict


class MultiDictSchema(Schema):
    """MultiDict aware schema used for loading e.g. request.args."""

    class Meta:
        """Throw away unknown values."""

        unknown = EXCLUDE

    LIST_TYPES = [
        fields.List,
    ]

    @classmethod
    def is_list_field(cls, field):
        """Method used to determine if a field is a list type field.

        This is used to unpack the MultiDict into a normal dictionary.
        """
        return any((isinstance(field, t) for t in cls.LIST_TYPES))

    @pre_load
    def flatten_multidict(self, data, **kwargs):
        """Flatten a MultiDict into a normal dictionary."""
        if not isinstance(data, MultiDict):
            return data
        data = data.to_dict(flat=False)

        for name, field in self.fields.items():
            if name in data and not self.is_list_field(field):
                data[name] = data[name][0]
        return data


class BaseListSchema(Schema):
    """List Schema for dumping extra information."""

    hits = fields.Method("get_hits")
    aggregations = fields.Method("get_aggs")
    links = fields.Method("get_links")
    sortBy = fields.Method("get_sorting_option")

    def get_hits(self, obj_list):
        """Apply hits transformation."""
        hits_list = []
        for obj in obj_list["hits"]["hits"]:
            hits_list.append(
                self.context["object_schema_cls"](context=self.context).dump(obj)
            )
        obj_list["hits"]["hits"] = hits_list
        return obj_list["hits"]

    def get_aggs(self, obj_list):
        """Apply aggregations transformation."""
        aggs = obj_list.get("aggregations")
        if not aggs:
            return missing
        return aggs

    def get_links(self, obj_list):
        """Apply links transformation."""
        links = obj_list.get("links")
        if not links:
            return missing
        return links

    def get_sorting_option(self, obj_list):
        """Apply sortBy transformation."""
        sortBy = obj_list.get("sortBy")
        if not sortBy:
            return missing
        return sortBy


class BaseObjectSchema(Schema):
    """Base Schema for dumping extra information."""

    def dump(self, obj, **kwargs):
        """Overriding marshmallow dump to dump extra key if any."""
        object_key = self.context.get("object_key", None)
        if object_key:
            obj[object_key] = Schema.dump(self, obj, **kwargs)
            return obj
        return Schema.dump(self, obj, **kwargs)
