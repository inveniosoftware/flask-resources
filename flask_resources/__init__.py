# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
#
# Flask-Resources is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Library for easily implementing REST APIs."""

from .resources import CollectionResource, Resource, ResourceConfig, SingletonResource
from .version import __version__

__all__ = (
    "__version__",
    "Resource",
    "ResourceConfig",
    "CollectionResource",
    "SingletonResource",
)
