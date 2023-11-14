# -*- coding: utf-8 -*-
#
# Copyright (C) 2023 CERN.
#
# Invenio-RDM is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.
""" TODO """

import yaml  # TODO pip install pyyaml


class Formatter:
    def to_bytes(self, dumped_item):
        raise NotImplementedError

    def to_bytes_list(self, dumped_item_list):
        raise NotImplementedError

    def to_str(self, dumped_item):
        raise NotImplementedError

    def to_str_list(self, dumped_item):
        raise NotImplementedError

    def to_etree(self, dumped_item):
        raise NotImplementedError

    def to_etree_list(self, dumped_item):
        raise NotImplementedError


class YAMLFormatter(Formatter):
    def serialize_object(self, obj):
        return yaml.dump(obj)

    def serialize_object_list(self, obj_list):
        return yaml.dump_all(obj_list)
