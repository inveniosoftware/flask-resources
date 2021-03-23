# -*- coding: utf-8 -*-
#
# Copyright (C) 2020-2021 CERN.
# Copyright (C) 2020-2021 Northwestern University.
#
# Flask-Resources is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Request parser for extracting URL args, headers and view args.

The request parser uses a declarative way to extract and validate request
parameters. The parser can parse data in three different locations:

- ``args``: URL query string (i.e. ``request.args``)
- ``headers``: Request headers (i.e. ``request.headers``)
- ``view_args``: Request view args (i.e. ``request.view_args``)

The parser is not meant to parse the request body. For that you should use the
``RequestBodyParser``.

The request parser can accept both a schema or a dictionary. Using the schema
enables you to do further pre/post-processing of values, while the dict version
can be more compact.

Example with schema:

.. code-block:: python

    class MyHeaders(ma.Schema):
        content_type = ma.fields.String()

    parser = RequestParser(MyHeaders, location='headers')
    parser.parse()

Same example with dict:

.. code-block:: python

    parser = RequestParser({
        'content_type': ma.fields.String()
    }, location='headers')
    parser.parse()

**URL args parsing**

If you are parsing URL args, be aware that a query string can have repeated
variables (e.g. in ``?type=a&type=b`` the value ``type`` is repeated).

Thus if you build your own schema for URL args, you should inherit from
``MultiDictSchema``. If you don't have repeated keys you can use a normal
Marshmallow schema.

**Unknown values**

If you pass a dict for the schema, you can control what to do with unknown
values:

.. code-block:: python

    parser = RequestParser({
        'id': ma.fields.String()
    }, location='args', unknown=ma.RAISE)
    parser.parse()

If you build your own schema, the same can be achieved with by providing the
meta class:

.. code-block:: python

    class MyArgs(ma.Schema):
        id = ma.fields.String()

        class Meta:
            unknown = ma.INCLUDE
"""

import marshmallow as ma
from flask import request

from .schema import MultiDictSchema


class RequestParser:
    """Request parser."""

    def __init__(self, schema_or_dict, location, unknown=ma.EXCLUDE):
        """Constructor.

        :param schema_or_dict: A marshmallow schema class or a mapping from
            keys to fields.
        :param location: Location where to load data from. Possible values:
            (``args``, ``headers``, or ``view_args``).
        :param unknown: Determines how to handle unknown values. Possible
            values: ``ma.EXCLUDE``, ``ma.INCLUDE``, ``ma.RAISE``. Only used if
            the schema is a dict.
        """
        assert location in ["args", "headers", "view_args"]
        self._location = location
        self._unknown = unknown

        if isinstance(schema_or_dict, dict):
            self._schema = self.schema_from_dict(schema_or_dict)
        else:
            self._schema = schema_or_dict

    @property
    def location(self):
        """The request location for this request parser."""
        return self._location

    @property
    def default_schema_cls(self):
        """Get the base schema class when dynamically creating the schema.

        By default, ``request.args`` is a MultiDict which a normal Marshmallow
        schema does not know how to handle, we therefore change the schema
        only for request args parsing.

        """
        if self._location == "args":
            return MultiDictSchema
        else:
            return ma.Schema

    def schema_from_dict(self, schema_dict):
        """Construct a schema from a dict."""
        cls_ = self.default_schema_cls

        class BaseSchema(cls_):
            class Meta:
                unknown = self._unknown

        return BaseSchema.from_dict(schema_dict)

    @property
    def schema(self):
        """Build the schema class."""
        return self._schema()

    def load_data(self):
        """Load data from request."""
        if self._location == "args":
            if issubclass(self._schema, MultiDictSchema):
                return request.args
            else:
                return request.args.to_dict(flat=False)
        elif self._location == "headers":
            return {
                k.lower().replace("-", "_"): v for (k, v) in request.headers.items()
            }
        elif self._location == "view_args":
            return request.view_args
        raise RuntimeError(f"Unknown request location: {self._location}.")

    def parse(self):
        """Parse the request data."""
        return self.schema.load(self.load_data())
