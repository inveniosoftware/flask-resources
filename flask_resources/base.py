# -*- coding: utf-8 -*-
#
# Copyright (C) 2025 Graz University of Technology.
#
# Flask-Resources is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Schema base."""


from marshmallow import Schema as BaseSchema


class Schema(BaseSchema):
    """Local wrapper for Schema to preserve context feature."""

    def __init__(self, *args, **kwargs):
        """Override constructor to squeeze in context"""
        context = kwargs.pop("context", {}) or {}
        super().__init__(*args, **kwargs)
        # it needs to be set here, otherwise the parent constructor would set
        # self.context to {}
        self.context = context

    def load(self, *args, **kwargs):
        """Override load to squeeze in context."""
        if context := kwargs.pop("context", None):
            self.context = context

        super().load(*args, **kwargs)
