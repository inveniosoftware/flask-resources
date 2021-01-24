# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
# Copyright (C) 2020 Northwestern University.
#
# Flask-Resources is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Library for easily implementing REST APIs."""

import warnings
from functools import wraps

import marshmallow as ma

from ..context import resource_requestctx


def select_request_parser(
    resource_method, config_parser_or_parsers, default_parser_cls
):
    """Returns request parser corresponding to situation."""
    if isinstance(config_parser_or_parsers, default_parser_cls):
        return config_parser_or_parsers

    return config_parser_or_parsers.get(
        resource_method,
        default_parser_cls(allow_unknown=False),  # default "parse nothing" parser
    )


def request_parser_decorator(parser_cls, config_attr, context_attr):
    """Decorator that parses the request object for the view."""

    def decorator(f):
        @wraps(f)
        def inner(self, *args, **kwargs):
            parser = select_request_parser(
                self.resource_method,
                getattr(self.resource.config, config_attr),
                parser_cls,
            )
            setattr(resource_requestctx, context_attr, parser.parse())
            return f(self, *args, **kwargs)

        return inner

    return decorator


class _ExcludeSchema(ma.Schema):
    class Meta:
        unknown = ma.EXCLUDE


class RequestParser:
    """Request parser.

    Base class for parsing request.
    """

    DEFAULT_SCHEMA_CLASS = _ExcludeSchema
    """The schema class to use if a dictionary is passed."""

    def __init__(self, schema=None, allow_unknown=None):
        """Constructor.

        :param schema: A marshmallow schema class or a mapping from keys to
        fields.
        """
        self._schema = schema
        self.allow_unknown = allow_unknown
        if allow_unknown is not None:
            warnings.warn(
                "The allow_unknown keyword argument is deprecated and has no "
                "effect. Use unknown values control on marshmallow instead.",
                DeprecationWarning,
            )

    @property
    def schema(self):
        """Build the schema class."""
        if self._schema is None:
            return None
        if isinstance(self._schema, dict):
            cls_ = self.DEFAULT_SCHEMA_CLASS
            if self.allow_unknown is True:
                # allow_unknown is deprecated (see __init__ above). Here we
                # add backward compatibility, so that when you pass a dict
                # you can use the allow_unknown keyword. Instead of using
                # allow_unknown you should now simply create a schema instead
                # and add the Meta class as show below:
                class _IncludeSchema(cls_):
                    class Meta:
                        unknown = ma.INCLUDE

                cls_ = _IncludeSchema

            return cls_.from_dict(self._schema)()
        else:
            return self._schema()

    def load_data(self):
        """Load data from request.

        This should be overwritten in subclasses to implement loading of data
        from the querystring, form values, headers etc.
        """
        raise NotImplementedError

    def parse(self):
        """Parse the request data."""
        if self.schema is None:
            return {}
        return self.schema.load(self.load_data())
