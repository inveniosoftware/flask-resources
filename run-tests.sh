#!/usr/bin/env sh
# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
#
# Flask-Resources is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

# Quit on errors
set -o errexit

# Quit on unbound symbols
set -o nounset

black --check --diff flask_resources tests
check-manifest --ignore ".*-requirements.txt"
sphinx-build -qnNW docs docs/_build/html
pytest
