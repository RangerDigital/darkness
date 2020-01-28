import pytest
import requests


def test_not_found(URL):
    # Check if custom 404 is working.
    response = requests.get(URL + "/hello")
    json = response.json()

    assert response.status_code == 404
    assert response.headers["Content-Type"] == "application/json"
    assert json["error"]


def test_invalid_method(URL):
    # Check if custom 405 is working.
    response = requests.get(URL + "/animations/blink")
    json = response.json()

    assert response.status_code == 405
    assert response.headers["Content-Type"] == "application/json"
    assert json["error"]
