# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
# Copyright (C) 2020 Northwestern University.
#
# Flask-Resources is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""Resources test module."""

import json


def test_base_resource(client):
    """Test the default resource."""
    # TODO: Only implement MethodView methods for defined Resource methods. Only then
    #       can we test that all methods return 405 (and not just the ones this library
    #       didn't define in its MethodViews
    headers = {"content-type": "application/json", "accept": "application/json"}

    # GET/Read a resource
    response = client.get("/resources/1234-ABCD", headers=headers)
    assert response.status_code == 200
    assert response.json == {}

    # PUT/Edit a resource
    obj_json = json.dumps({"id": "1234-ABCD", "content": "something new"})
    response = client.put("/resources/1234-ABCD", data=obj_json, headers=headers)
    assert response.status_code == 200
    assert response.json == {}

    # PATCH/Partial edit a resource
    ops_json = json.dumps(
        {"op": "replace", "path": "/content", "value": "something patched"}
    )
    response = client.patch("/resources/1234-ABCD", data=obj_json, headers=headers)
    assert response.status_code == 200
    assert response.json == {}

    # DELETE/remove a resource
    response = client.delete("/resources/1234-ABCD", headers=headers)
    assert response.status_code == 200
    assert response.json == {}


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

    # Get the previously created obj using default headers
    resource_obj = client.get("/custom/1234-ABCD")
    assert resource_obj.status_code == 200
    assert resource_obj.json["id"] == "1234-ABCD"

    # Delete the previously created obj
    resource_obj = client.delete("/custom/1234-ABCD", headers=headers)
    assert resource_obj.status_code == 200
    assert resource_obj.json == {}

    # PUT/Edit a list of resource units
    obj_json = json.dumps([{"id": "1234-ABCD", "content": "updated content"}])
    response = client.put("/custom/", data=obj_json, headers=headers)
    assert response.status_code == 200
    assert response.json == [{"id": "1234-ABCD", "content": "updated content"}]

    # DELETE/remove a list of resource units
    response = client.delete("/custom/", headers=headers)
    assert response.status_code == 200
    assert response.json == []
