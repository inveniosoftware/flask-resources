#!/usr/bin/env sh
# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
#
# Flask-Resources is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

pydocstyle flask_resources tests docs && \
isort --multi-line=3 --line-width=88 --trailing-comma --force-grid-wrap=0 --use-parentheses -rc -c -df && \
black --check --diff flask_resources && \
check-manifest --ignore ".travis-*" && \
sphinx-build -qnNW docs docs/_build/html && \
pytest
