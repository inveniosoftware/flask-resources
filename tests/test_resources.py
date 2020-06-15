# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
#
# Flask--Resources is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""Resources test module."""

import json


def test_base_resourece(base_client):
    """Test the default resource."""
    headers = {"content-type": "application/json", "accept": "application/json"}

    # GET/Read a resource
    resource_obj = base_client.get("/resources/1234-ABCD", headers=headers)
    assert resource_obj.status_code == 405

    # PUT/Edit a resource
    obj_json = json.dumps({"id": "1234-ABCD", "content": "something new"})
    resource_obj = base_client.get(
        "/resources/1234-ABCD", data=obj_json, headers=headers
    )
    assert resource_obj.status_code == 405

    # PATCH/Partial edit a resource
    ops_json = json.dumps(
        {"op": "replace", "path": "/content", "value": "something patched"}
    )
    resource_obj = base_client.get("/resources/1234-ABCD", headers=headers)
    assert resource_obj.status_code == 405

    # DELETE/remove a resource
    resource_obj = base_client.get(
        "/resources/1234-ABCD", data=obj_json, headers=headers
    )
    assert resource_obj.status_code == 405


def test_custom_resource(base_client):
    """Test a custom resource."""
    headers = {"content-type": "application/json", "accept": "application/json"}

    # The resource returns a list, empty for now
    resource_obj = base_client.get("/custom/", headers=headers)
    assert resource_obj.status_code == 200
    assert len(resource_obj.get_json()) == 0

    # Create a resource object
    obj_content = {"id": "1234-ABCD", "content": "test resource obj content"}
    obj_json = json.dumps(obj_content)
    resource_obj = base_client.post("/custom/", data=obj_json, headers=headers)
    assert resource_obj.status_code == 201

    # Search for the previously created obj
    resource_obj = base_client.get("/custom/", headers=headers)
    assert resource_obj.status_code == 200

    resource_obj_json = resource_obj.get_json()
    assert len(resource_obj.get_json()) == 1
    assert resource_obj_json[0]["id"] == "1234-ABCD"

    # Get the previously created obj
    resource_obj = base_client.get("/custom/1234-ABCD", headers=headers)
    assert resource_obj.status_code == 200

    resource_obj_json = resource_obj.get_json()
    assert resource_obj_json["id"] == "1234-ABCD"