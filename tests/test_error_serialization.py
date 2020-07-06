import pytest
from flask import Flask, request
from werkzeug.exceptions import BadRequest, UnsupportedMediaType

from flask_resources.context import resource_requestctx
from flask_resources.resources import CollectionResource, ResourceConfig


class ErrorConfig(ResourceConfig):
    """ErrorResource configuration."""

    item_route = "/error/<int:error_code>"
    list_route = "/error/"


class ErrorResource(CollectionResource):
    """Error returning resource implementation."""

    default_config = ErrorConfig

    def item_error(self):
        """Raise an error."""
        error_code = resource_requestctx.route["error_code"]
        if error_code == 415:
            raise UnsupportedMediaType()
        elif error_code == 400:
            raise BadRequest()

    def list_error(self):
        """Raise an error."""
        # TODO: Make it easier to get request.args into resource_requestctx by default
        error_code = request.args["error_code"]
        if error_code == "415":
            raise UnsupportedMediaType()
        elif error_code == "400":
            raise BadRequest()
        return ([],)

    def search(self, *args, **kwargs):
        """Perform a search over the items."""
        return self.list_error()

    def create(self, *args, **kwargs):
        """Create an item."""
        self.list_error()

    def read(self, *args, **kwargs):
        """Read an item."""
        self.item_error()

    def update(self, *args, **kwargs):
        """Update an item."""
        self.item_error()

    def partial_update(self, *args, **kwargs):
        """Partial update an item."""
        self.item_error()

    def delete(self, *args, **kwargs):
        """Delete an item."""
        self.item_error()


@pytest.fixture(scope="module")
def app():
    """Application factory fixture."""
    app_ = Flask(__name__)
    custom_bp = ErrorResource().as_blueprint("error_resource")
    app_.register_blueprint(custom_bp)
    return app_


def test_errors_are_json_serialized_by_default(client):
    headers = {"accept": "application/json", "content-type": "application/json"}

    # Test these common error codes on same endpoint
    res = client.get("/error/415", headers=headers)
    assert res.status_code == 415
    assert res.json["status"] == 415
    assert res.json["message"] is not None

    res = client.get("/error/400", headers=headers)
    assert res.status_code == 400
    assert res.json["status"] == 400
    assert res.json["message"] is not None


def test_serialization_of_exceptional_error_406(client):
    # NOTE: 406 can be raised before we have a response_handler: this means we can't
    #       serialize a response body
    headers = {"accept": "application/json+garbage"}  # this triggers the error

    res = client.get("/error/406", headers=headers)
    assert res.status_code == 406
    assert res.json is None


def test_all_endpoints_serialize_errors(client):
    headers = {"accept": "application/json", "content-type": "application/json"}

    # search
    res = client.get("/error/?error_code=400", headers=headers)
    assert res.status_code == 400
    assert res.json["status"] == 400
    assert res.json["message"] is not None

    # create
    res = client.post("/error/?error_code=400", headers=headers)
    assert res.status_code == 400
    assert res.json["status"] == 400
    assert res.json["message"] is not None

    # read
    res = client.put("/error/400", headers=headers)
    assert res.status_code == 400
    assert res.json["status"] == 400
    assert res.json["message"] is not None

    # update
    res = client.put("/error/400", headers=headers)
    assert res.status_code == 400
    assert res.json["status"] == 400
    assert res.json["message"] is not None

    # partial update
    res = client.patch("/error/400", headers=headers)
    assert res.status_code == 400
    assert res.json["status"] == 400
    assert res.json["message"] is not None

    # delete
    res = client.delete("/error/400", headers=headers)
    assert res.status_code == 400
    assert res.json["status"] == 400
    assert res.json["message"] is not None
