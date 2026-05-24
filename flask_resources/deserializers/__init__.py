# SPDX-FileCopyrightText: 2020-2021 CERN.
# SPDX-FileCopyrightText: 2020-2021 Northwestern University.
# SPDX-License-Identifier: MIT

"""Deserializers."""

from .base import DeserializerMixin
from .json import JSONDeserializer

__all__ = ("JSONDeserializer", "DeserializerMixin")
