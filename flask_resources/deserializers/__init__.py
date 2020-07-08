# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
#
# Flask-Resources is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Deserializers."""

from .deserializers import DeserializerMixin
from .json import JSONDeserializer

__all__ = ("JSONDeserializer", "DeserializerMixin")
