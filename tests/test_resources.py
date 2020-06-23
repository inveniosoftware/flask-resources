# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
#
# Flask--Resources is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""Resources test module."""

import json

method_not_allowed_str = "The method is not allowed for the requested URL."


def test_base_resourece(client):
    """Test the default resource."""
    headers = {"content-type": "application/json", "accept": "application/json"}

    # GET/Read a resource
    resource_obj = client.get("/resources/1234-ABCD", headers=headers)
    assert resource_obj.status_code == 405
    assert resource_obj.json == method_not_allowed_str

    # PUT/Edit a resource
    obj_json = json.dumps({"id": "1234-ABCD", "content": "something new"})
    resource_obj = client.put("/resources/1234-ABCD", data=obj_json, headers=headers)
    assert resource_obj.status_code == 405
    assert resource_obj.json == method_not_allowed_str

    # PATCH/Partial edit a resource
    ops_json = json.dumps(
        {"op": "replace", "path": "/content", "value": "something patched"}
    )
    resource_obj = client.patch("/resources/1234-ABCD", data=obj_json, headers=headers)
    assert resource_obj.status_code == 405
    assert resource_obj.json == method_not_allowed_str

    # DELETE/remove a resource
    resource_obj = client.delete("/resources/1234-ABCD", headers=headers)
    assert resource_obj.status_code == 405
    assert resource_obj.json == method_not_allowed_str


def test_custom_resource(client):
    """Test a custom resource."""
    headers = {"content-type": "application/json", "accept": "application/json"}

    # The resource returns a list, empty for now
    resource_obj = client.get("/custom/", headers=headers)
    assert resource_obj.status_code == 200
    assert len(resource_obj.json) == 0

    # Create a resource object
    obj_content = {"id": "1234-ABCD", "content": "test resource obj content"}
    obj_json = json.dumps(obj_content)
    resource_obj = client.post("/custom/", data=obj_json, headers=headers)
    assert resource_obj.status_code == 201

    # Search for the previously created obj
    resource_obj = client.get("/custom/", headers=headers)
    assert resource_obj.status_code == 200
    assert len(resource_obj.json) == 1
    assert resource_obj.json[0]["id"] == "1234-ABCD"

    # Get the previously created obj
    resource_obj = client.get("/custom/1234-ABCD", headers=headers)
    assert resource_obj.status_code == 200
    assert resource_obj.json["id"] == "1234-ABCD"

    # Delete the previously created obj
    resource_obj = client.delete("/custom/1234-ABCD", headers=headers)
    assert resource_obj.status_code == 200
    assert resource_obj.json == {}
