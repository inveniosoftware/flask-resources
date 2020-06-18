# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
#
# Flask--Resources is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""Resources test module."""

import json
from unittest.mock import Mock

import pytest
from flask import Flask
from werkzeug.exceptions import NotFound

from flask_resources.resources import CollectionResource, ResourceConfig, \
    SingletonResource

# Notes
# - Resource().create has no parameters which is weird
#   At least *args, **kwargs   --- mentioned by Lars
# - Even as API creator I need to provide a Config separately
#   --> little strange
#   --> little confusing bc now there will be the library's config and the application's
#       config
# - TODO: Resource should check global config to override the used ResourceConfig
#         This is the hook to let others configure this API, rihgt?
# - create() method must return a serializable object : must be indicated
# - Would be nice if create() method defaulted to 201 status code (nice-to-have)
# - We should just follow the body,status,headers return of Flask
# - For post, I need to implement "create" method... why not have to implement 'post'
#   method:
#     * because you can post to an item and post to a collection (and post to an action)
#       ~ maybe better get_item, get_list, post_item, post_list, post_action ...
# - default to json is a little bit magic
# - parameters to create/read... are magic
#   * read: comes from URL route - which may have a name that clobbers a builtin...
# - DepositResource is created once only ...
# - if put not defined it should return 405: returns 400 because loading is done first
#    - we can't really rely on running the method because it may have side-effects
#    - this might not be possible with current implementation
# - because loading and matching to paramter is magic, we don't know where the
#   parameters are coming from
#   e.g. PUT /records/<id>/draft {id: "1234-ABCD"}
#        def update(self, id, data) breaks (should be reverse)
#        PUT /records/<data>/draft
#        def update(self, data) breaks because of name clash
#        TypeError: update() got an unexpected keyword argument 'id'
# - 404 or 405 take precedence: 404 I think
# - attach actions to same resource would be much better ux
#   * can do via decorator I think... might get messy with other decorators:
#   @action()
#   def actionA()
# - having to define __init__ to pass configuration is heavy
# ```python
# class DepositActionResource(SingletonResource):
#     default_config = ResourceConfig
# ```
# seems lighter
# - list_route for SingletonResource is confusing
#   - action for an item like we need is not possible right now
# - why collectionresource different than resource? Could we combine both into 1?
#   Unimplemented route should return appropriate HTTP code anyway
# - collections.py L40 search is missing request_context -> goes back to the discussion
#   about deserialization
# - if deserializer for potential Accept MIMEtype is not defined, get obj None
# - decorators on MethodView apply to all view methods, so we don't want that if
#   possible (and it is possible, flask-restful does it)
# ------------------------------- SENT --------------------------#

# As Deposit API creator
class DepositConfig(ResourceConfig):
    """Base resource configuration."""

    item_route = "/records/<id>/draft"
    list_route = "/records/"
    # item_request_loaders = {
    #     "application/json": JSONLoader(),
    #     "application/json+patch": JSONPatchLoader(),
    # }
    # item_response_handlers = {
    #     "application/json": ItemResponse(JSONSerializer())
    # }
    # list_response_handlers = {
    # "application/json": ListResponse(JSONSerializer())}
    # create_request_parser = create_request_parser
    # item_request_parser = item_request_parser
    # search_request_parser = search_request_parser
    # create_request_parser = lambda *args, **kwargs: Mock()
    # item_request_parser = lambda *args, **kwargs: Mock()
    # search_request_parser = lambda *args, **kwargs: Mock()
    #     headers = {"content-type": "application/json", "accept": "application/json"}


backend_db = {}


# As Deposit API creator
class DepositResource(CollectionResource):
    """Custom resource implementation."""

    def __init__(self, config=DepositConfig, *args, **kwargs):
        """Constructor."""

        super(DepositResource, self).__init__(config, *args, **kwargs)
        self.db = backend_db

    # get_list
    # def search(self, request_context):
    #     """Perform a search over the items."""
    #     query = resource_requestctx.request_args.get("q", "")
    #     resp = []
    #     for key, value in self.db.items():
    #         if query in key or query in value:
    #             resp.append({"id": key, "content": value})
    #     return 200, resp

    # post_item
    def create(self, obj):
        """Create."""
        # At this point the body has been deserialized
        self.db[obj["id"]] = obj["content"]
        return 201, obj

    # get_item
    def read(self, id):
        """Read."""
        # At this point the URL has been deserialized
        _id = id
        return 200, {"id": _id, "content": self.db[_id]}

    # put_item
    def update(self, data, id):
        """Update."""
        # At this point the URL has been deserialized
        # At this point the URL + body has been deserialized
        _id = id
        if _id not in self.db:
            raise NotFound()
        else:
            self.db[data["id"]] = data["content"]
            return 200, {"id": _id, "content": self.db[_id]}


class DepositActionConfig(ResourceConfig):
    list_route = "/records/<id>/actions/publish"


class DepositActionResource(SingletonResource):
    def __init__(self, config=DepositConfig, *args, **kwargs):
        """Constructor."""
        super(DepositActionResource, self).__init__(config, *args, **kwargs)


class RecordsConfig(ResourceConfig):
    list_route = "/records/<id>/actions/publish"


backend_records_db = {}


class RecordsResource(CollectionResource):
    def __init__(self, config=RecordsConfig, *args, **kwargs):
        """Constructor."""
        super(RecordsResource, self).__init__(config, *args, **kwargs)
        self.db = backend_records_db


@pytest.fixture(scope="module")
def app():
    """Flask App fixture."""
    app_ = Flask(__name__)
    bp = DepositResource().as_blueprint("deposit_resource")
    app_.register_blueprint(bp)

    bp = DepositActionResource().as_blueprint("deposit_action_resource")
    app_.register_blueprint(bp)

    return app_


# | Action  |               Endpoint               |      Description      |
# |:-------:|--------------------------------------|:---------------------:|
# | **Records** | | |
    # | GET     | /records                             | Search (published) records          |  # noqa
# | GET     | /records/:id                         | Get a record         |
# | DELETE  | /records/:id                         | Delete a record      |
# | **Draft** | | |
    # | POST    | /records                             | Create new draft for new record from nothing |  # noqa
# | POST    | /records/:id/draft                   | Create new draft for existing record from existing record (i.e. new edit) |  # noqa
    # | GET     | /records/:id/draft                   | Get a draft (created from all the above ways) |  # noqa
    # | PUT     | /records/:id/draft                   | Update draft          |
# | DELETE  | /records/:id/draft                   | Discard a draft/delete a new record            |  # noqa
# | **Actions** | | |
# | POST    | /records/:id/draft/actions/:action   | Execute action |
    # | POST    | /records/:id/draft/actions/publish   | Publish draft to record (example of row above) |  # noqa
# | **Drafts + Records** | | |
# | GET     | /user/records                       | Search and display mix of records and drafts |  # noqa
# | **Versions** | | |
# | POST    | /records/:id/versions                | Create new draft for new record from existing record (i.e. new version)|  # noqa
# | GET     | /records/:id/versions                | Search versions of the record |

@pytest.fixture
def cleardb():
    global backend_db, backend_records_db
    backend_db.clear()
    backend_records_db.clear()
    print("cleardb called")


# test deposit post json
def test_post_create_draft(client, cleardb):
    """Test POST /records."""

    headers = {
        "content-type": "application/json", "accept": "application/json"
    }

    # Create a resource object
    obj_content = {"id": "1234-ABCD", "content": "test resource obj content"}
    obj_json = json.dumps(obj_content)
    response = client.post(
        "/records/",
        data=obj_json,
        headers=headers
    )

    assert response.status_code == 201


# test deposit get json
def test_get_return_draft(client, cleardb):
    # Search for the previously created obj
    headers = {
        "content-type": "application/json", "accept": "application/json"
    }
    # Create a resource object
    obj_content = {"id": "1234-ABCD", "content": "test resource obj content"}
    obj_json = json.dumps(obj_content)
    response = client.post(
        "/records/",
        data=obj_json,
        headers=headers
    )

    response = client.get("/records/1234-ABCD/draft", headers=headers)

    assert response.status_code == 200
    assert {
        "id": "1234-ABCD",
        "content": "test resource obj content"
    } == response.json


# test deposit put json
def test_put_error_on_absent_draft(client, cleardb):
    headers = {
        "content-type": "application/json", "accept": "application/json"
    }
    obj_content = {"id": "1234-ABCD", "content": "test PUT on resource obj content"}
    obj_json = json.dumps(obj_content)

    response = client.put(
        "/records/1234-ABCD/draft",
        data=obj_json,
        headers=headers
    )
    assert response.status_code == 404  # Original wasn't created


def test_put_update_draft(client, cleardb):
    headers = {
        "content-type": "application/json", "accept": "application/json"
    }
    # Create first
    obj_content = {"id": "1234-ABCD", "content": "post content"}
    obj_json = json.dumps(obj_content)

    response = client.post(
        "/records/",
        data=obj_json,
        headers=headers
    )
    assert response.status_code == 201

    # Then update
    obj_content = {"id": "1234-ABCD", "content": "put content"}
    obj_json = json.dumps(obj_content)

    response = client.put(
        "/records/1234-ABCD/draft",
        data=obj_json,
        headers=headers
    )

    assert response.status_code == 200
    assert {
        "id": "1234-ABCD",
        "content": "put content"
    } == response.json


# SKIP BROKEN
# test deposit action json  --> skip bc doesn't work
# def test_post_publish_draft_to_record(client, cleardb):
#     headers = {
#         "content-type": "application/json", "accept": "application/json"
#     }
#     # Create
#     obj_content = {"id": "1234-ABCD", "content": "post content"}
#     obj_json = json.dumps(obj_content)
#     response = client.post(
#         "/records/",
#         data=obj_json,
#         headers=headers
#     )
#     assert response.status_code == 201

#     # Then publish
#     headers['Etag'] = "qwerty123"
#     response = client.post(
#         "/records/1234-ABCD/draft/actions/publish",
#         headers=headers
#     )

#     assert response.status_code == 201
#     assert {
#         "id": "1234-ABCD",
#         "content": "post content"
#     } == response.json


# SKIP BROKEN
# test deposit list json
# def test_get_list_records(client, cleardb):
#     global backend_records_db
#     headers = {
#         "content-type": "application/json", "accept": "application/json"
#     }
#     # Prime backend
#     backend_records_db.update({"1234-ABCD": "published content"})

# #     obj_content = {"id": "1234-ABCD", "content": "post content"}
# #     obj_json = json.dumps(obj_content)
#     response = client.get(
#         "/records/",
#         headers=headers
#     )
#     assert response.status_code == 200
#     assert [{
#         "id": "1234-ABCD",
#         "content": "published content"
#     }] == response.json
#     print("response.headers", response.headers)
#     assert False


# SKIP BROKEN
# test deposit create xml
# def test_post_create_draft_xml(client, cleardb):
#     headers = {
#         "content-type": "application/xml", "accept": "application/xml"
#     }
#     xml_data = (
#         "<root><id>1234-ABCD</id><content>test resource obj content</content></root>"
#     )
#     response = client.post(
#         "/records/",
#         data=xml_data,
#         headers=headers
#     )

#     assert response.status_code == 201
