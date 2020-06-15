# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
#
# Flask--Resources is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""Resources test module."""


def test_custom_resource(base_client):
    """Test the registration of a custom resource.

    It tests the registration process itself and the correct functioning
    of its endpoints.
    """
    # The resource returns a list, empty for now
    resource_obj = base_client.get("/resources/")
    assert resource_obj.status_code == 200
    assert len(resource_obj.get_json) == 0

    # Create a resource object
    obj_content = {"id": "1234-ABDC", "content": "test resource obj content"}
    resource_obj = base_client.post("/resources/", body=obj_content)
    assert resource_obj.status_code == 201

    # Search for the previously created obj
    resource_obj = base_client.get("/resources/")
    assert resource_obj.status_code == 200

    resource_obj_json = resource_obj.get_json()
    assert len(resource_obj.data) == 1
    assert resource_obj_json[0]["id"] == "1234-ABCD"

    # Get the previously created obj
    resource_obj = base_client.get("/resources/1234-ABDC")
    assert resource_obj.status_code == 200

    resource_obj_json = resource_obj.get_json()
    assert resource_obj_json["id"] == "1234-ABCD"
