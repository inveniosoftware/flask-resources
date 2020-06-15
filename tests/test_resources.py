# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
#
# Flask--Resources is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""Resources test module."""

import json


def test_custom_resource(base_client):
    """Test the registration of a custom resource.

    It tests the registration process itself and the correct functioning
    of its endpoints.
    """
    headers = {"content-type": "application/json", "accept": "application/json"}

    # The resource returns a list, empty for now
    resource_obj = base_client.get("/resources/", headers=headers)
    assert resource_obj.status_code == 200
    assert len(resource_obj.get_json()) == 0

    # Create a resource object
    obj_content = {"id": "1234-ABCD", "content": "test resource obj content"}
    obj_json = json.dumps(obj_content)
    resource_obj = base_client.post("/resources/", data=obj_json, headers=headers)
    assert resource_obj.status_code == 201

    # Search for the previously created obj
    resource_obj = base_client.get("/resources/", headers=headers)
    assert resource_obj.status_code == 200

    resource_obj_json = resource_obj.get_json()
    assert len(resource_obj.get_json()) == 1
    assert resource_obj_json[0]["id"] == "1234-ABCD"

    # Get the previously created obj
    resource_obj = base_client.get("/resources/1234-ABCD", headers=headers)
    assert resource_obj.status_code == 200

    resource_obj_json = resource_obj.get_json()
    assert resource_obj_json["id"] == "1234-ABCD"
