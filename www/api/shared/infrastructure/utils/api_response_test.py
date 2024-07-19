from flask import Response

from .api_response import api_response


def test_api_response():
    response = api_response('{"message": "Hello, World!"}')
    assert isinstance(response, Response)
    assert response.status_code == 200
    assert response.mimetype == 'application/json'
    assert response.data == b'{"message": "Hello, World!"}'
