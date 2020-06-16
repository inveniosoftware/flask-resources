# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
#
# Flask-Resources is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Loaders."""

from .json import JSONLoader, JSONPatchLoader
from .loaders import LoaderMixin

__all__ = ("JSONLoader", "JSONPatchLoader", "LoaderMixin")
