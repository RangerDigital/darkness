import pytest
import requests


def test_not_found(URL):
    # Check if custom 404 is working.
    response = requests.get(URL + "/hello")
    json = response.json()

    assert response.status_code == 404
    assert response.headers["Content-Type"] == "application/json"
    assert json["error"] == "Endpoint with that URL doesn't exist!"

# I need to change this file to run tests
