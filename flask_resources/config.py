# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 CERN.
# Copyright (C) 2021 Northwestern University.
#
# Flask-Resources is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Small utilities to resolve values from the resource configuration."""


class ConfigAttrValue:
    """Represents a value to be resolved from a config."""

    def __init__(self, config_attr):
        """Store the config attribute name."""
        self.config_attr = config_attr

    def resolve(self, config):
        """Resolve the configuration value."""
        return getattr(config, self.config_attr)


def resolve_from_conf(val, config):
    """Resolve the given value from config if needed."""
    if isinstance(val, ConfigAttrValue):
        return val.resolve(config)
    return val


def from_conf(config_attr):
    """Helper to create a config resolved value."""
    return ConfigAttrValue(config_attr)
