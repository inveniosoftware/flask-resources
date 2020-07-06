# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
#
# Flask-Resources is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Library for easily implementing REST APIs."""

from ..errors import SearchPaginationRESTError


def build_pagination(request_args):
    """Build pagination."""
    pagination = {}
    if request_args.get("page") and request_args.get("from"):
        raise SearchPaginationRESTError(
            messages="The query parameters from and page must not be "
            "used at the same time.",
            description="Invalid pagination parameters.",
            field_names=["page", "from"],
        )

    # Default if neither page nor from is specified
    if not (request_args.get("page") or request_args.get("from")):
        request_args["page"] = 1

    if request_args.get("page"):
        pagination.update(
            dict(
                from_idx=(request_args["page"] - 1) * request_args["size"],
                to_idx=request_args["page"] * request_args["size"],
                links=dict(
                    prev={"page": request_args["page"] - 1},
                    self={"page": request_args["page"]},
                    next={"page": request_args["page"] + 1},
                ),
            )
        )
    elif request_args.get("from"):
        pagination.update(
            dict(
                from_idx=request_args["from"] - 1,
                to_idx=request_args["from"] - 1 + request_args["size"],
                links=dict(
                    prev={"from": max(1, request_args["from"] - request_args["size"])},
                    self={"from": request_args["from"]},
                    next={"from": request_args["from"] + request_args["size"]},
                ),
            )
        )

    # Modify original dict
    request_args["pagination"] = pagination
