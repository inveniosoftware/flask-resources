# -*- coding: utf-8 -*-
#
# Copyright (C) 2024-2024 CERN.
#
# Flask-Resources is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""CSV serializer."""

import csv

from .base import BaseSerializer


class Line(object):
    """Object that implements an interface the csv writer accepts."""

    def __init__(self):
        """Initialize."""
        self._line = None

    def write(self, line):
        """Write a line."""
        self._line = line

    def read(self):
        """Read a line."""
        return self._line


class CSVSerializer(BaseSerializer):
    """CSV serializer for records.

    Note: This serializer is not suitable for serializing large number of
    records.
    """

    def __init__(self, *args, **kwargs):
        """Initialize CSVSerializer.

        :param csv_excluded_fields: list of paths of the fields that
                                    should be excluded from the final output
        :param csv_included_fields: list of paths of the only fields that
                                    should be included in the final output
        :param header_separator: separator that should be used when flattening
                                 nested dictionary keys
        :param collapse_lists: prevent lists being expanded into many columns
                               and instead newline seperated fields
        """
        self.csv_excluded_fields = kwargs.pop("csv_excluded_fields", [])
        self.csv_included_fields = kwargs.pop("csv_included_fields", [])

        if self.csv_excluded_fields and self.csv_included_fields:
            raise ValueError("Please provide only fields to either include or exclude")

        self.header_separator = kwargs.pop("header_separator", "_")

        self.collapse_lists = kwargs.pop("collapse_lists", False)

    def serialize_object(self, obj):
        """Serialize a single record and persistent identifier.

        :param pid: Persistent identifier instance.
        :param record: Record instance.
        :param links_factory: Factory function for record links.
        """
        record = self.process_dict(obj)

        return self._format_csv([record])

    def serialize_object_list(self, obj_list):
        """Dump the object list into a csv string."""
        records = [self.process_dict(obj) for obj in obj_list["hits"]["hits"]]
        return self._format_csv(records)

    def process_dict(self, dictionary):
        """Transform record dict with nested keys to a flat dict."""
        return self._flatten(dictionary)

    def _format_csv(self, records):
        """Return the list of records as a CSV string."""
        # build a unique list of all records keys as CSV headers
        if self.csv_included_fields:
            headers = self.csv_included_fields
        else:
            headers = set()
            for rec in records:
                headers.update(rec.keys())
            headers = sorted(headers)

        # write the CSV output in memory
        line = Line()
        writer = csv.DictWriter(line, fieldnames=headers)
        writer.writeheader()
        result = line.read()

        for record in records:
            writer.writerow(record)
            result += line.read()

        return result

    def _flatten(self, value, parent_key=""):
        """Flattens nested dict recursively, skipping excluded fields."""
        items = []
        sep = self.header_separator if parent_key else ""

        if isinstance(value, dict):
            for k, v in value.items():
                # for dict, build a key field_subfield, e.g. title_subtitle
                new_key = parent_key + sep + k
                if self.is_field_included(new_key):
                    items.extend(self._flatten(v, new_key).items())
        elif isinstance(value, list):
            if not self.collapse_lists:
                for index, item in enumerate(value):
                    # for lists, build a key with an index, e.g. title_0_subtitle
                    new_key = parent_key + sep + str(index)
                    if self.is_field_included(new_key):
                        items.extend(self._flatten(item, new_key).items())
            else:
                # for collapsed lists do not include index, e.g. title_subtitle
                new_key = parent_key
                if self.is_field_included(new_key):
                    if all([isinstance(v, str) for v in value]):
                        values = "\n".join(value)
                        items.append((new_key, values))
                    else:
                        items.extend(self._flatten_list_dict(value, new_key).items())

        else:
            if self.is_field_included(parent_key):
                items.append((parent_key, value))

        return dict(items)

    def _flatten_list_dict(self, value, parent_key=""):
        combined_dict = {}
        iterator = 0
        keys = set()
        for item in value:
            current_keys = set()
            for k, v in item.items():
                if isinstance(v, dict):
                    return self._flatten_list_dict_dict(value, parent_key)
                new_key = f"{parent_key}.{k}" if parent_key else k
                if self.is_field_included(new_key):
                    current_keys.add(new_key)
                    if new_key in keys:
                        combined_dict[new_key].append(v)
                    else:
                        keys.add(new_key)
                        if iterator > 0:
                            combined_dict[new_key] = [""] * iterator + [v]
                        else:
                            combined_dict[new_key] = [v]

            missing_keys = keys - current_keys
            for missing_key in missing_keys:
                combined_dict[missing_key].append("")

            iterator += 1

        flattened_items = [
            (key, "\n".join(map(str, values))) for key, values in combined_dict.items()
        ]

        return dict(flattened_items)

    def _flatten_list_dict_dict(self, value, parent_key=""):
        # Combine the dictionaries in the list into a single dictionary
        combined_dict = {}
        iterator = 0
        keys = set()
        for item in value:
            current_keys = set()
            for k1, v1 in item.items():
                if isinstance(v1, str):
                    new_key = f"{parent_key}.{k1}" if parent_key else f"{k1}"
                    if self.is_field_included(new_key):
                        combined_dict[new_key] = [v1]
                else:
                    if not isinstance(v1, dict):
                        continue
                    for k2, v2 in v1.items():
                        if not isinstance(v2, str):
                            continue
                        new_key = (
                            f"{parent_key}.{k1}.{k2}" if parent_key else f"{k1}.{k2}"
                        )
                        if self.is_field_included(new_key):
                            current_keys.add(new_key)
                            if new_key in keys:
                                combined_dict[new_key].append(v2)
                            else:
                                keys.add(new_key)
                                if iterator > 0:
                                    combined_dict[new_key] = [""] * iterator + [v2]
                                else:
                                    combined_dict[new_key] = [v2]

            missing_keys = keys - current_keys
            for missing_key in missing_keys:
                combined_dict[missing_key].append("")

            iterator += 1

        # Flatten the combined dictionary
        flattened_items = [
            (key, "\n".join(map(str, values))) for key, values in combined_dict.items()
        ]
        return dict(flattened_items)

    def is_field_included(self, key):
        """Determines if a key should be included or not."""
        if key in self.csv_excluded_fields:
            return False
        if self.csv_included_fields and not self.key_in_field(
            key, self.csv_included_fields
        ):
            return False
        return True

    def key_in_field(self, key, fields):
        """Checks if the given key is contained within any of the fields."""
        for field in fields:
            if key in field:
                return True
        return False
