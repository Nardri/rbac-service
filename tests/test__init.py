"""Module to test for the flask application"""

import json


def test_flask_application(client):
    """Should pass if the application starts successfully.
    Args:
        client (func): Flask test client
    Returns:
        None
    """

    response_raw = client.get('/')
    response_json = json.loads(response_raw.data)
    assert response_json['data'] == {
        'message': 'Role Based Access Control Service.',
        'status': 'success'
    }
