# -*- coding: utf-8 -*-
#
# Copyright (C) 2023 CERN.
#
# Invenio-RDM is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.
""" TODO """

from .yaml import Formatter
from lxml import etree
import xmltodict

class XMLFormatter(Formatter):
    _namespaces = None

    @property
    def namespaces(self):
        return self._namespaces

    def __init__(self, **kwargs):
        super().__init__()
        if "namespaces" in kwargs:
            self._namespaces = kwargs["namespaces"]

        self.bootstrap = self._build_bootstrap()

    def _build_bootstrap(self):
        xml_tag = f"""<?xml version="1.0"?>"""
        return xml_tag

    def serialize_object(self, obj):
        return self.to_str(self.to_etree(obj))

    def to_etree(self, obj):
        if isinstance(obj, dict):
            keys = list(obj.keys())
            # Dict has only one root
            assert len(keys) == 1

            root = keys[0]
            if self.namespaces:
                for k, v in self.namespaces.items():
                    if k == "default":
                        obj[root][f"@xmlns"] = v
                    else:
                        obj[root][f"@xmlns:{k}"] = v
            _etree = etree.fromstring(xmltodict.unparse(obj).encode("utf-8"))
        elif isinstance(obj, str):
            _etree = etree.fromstring(obj.encode("utf-8"))
        else:
            raise TypeError("Invalid type to create etree: expected str or dict.")

        return _etree

    def to_str(self, obj):
        return etree.tostring(obj, xml_declaration=True, encoding="utf-8")
