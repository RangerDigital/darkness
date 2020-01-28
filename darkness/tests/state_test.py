import pytest
import requests


def test_get(URL):
    # Check if state has all values.
    response = requests.get(URL + "/state")
    json = response.json()

    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"

    assert set(("status", "hue", "saturation", "value")) <= set(json)


def test_post(URL):
    # Check if you can update state with some correct values.
    payload = {"hue": 35, "saturation": 0.5}

    response = requests.post(URL + "/state", json=payload)
    json = response.json()

    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"

    assert json["hue"] == payload["hue"]
    assert json["saturation"] == payload["saturation"]

    assert set(("status", "hue", "saturation", "value")) <= set(json)


def test_invalid_values_post(URL):
    # Check if you can update state with some invalid values.
    payload = {"hue": -234, "saturation": 6.5}

    response = requests.post(URL + "/state", json=payload)

    assert response.status_code == 400


def test_invalid_types_post(URL):
    # Check if you can update state with some invalid types.
    payloads = [{"hue": "21=Hello"}, {"saturation": "23=Hello"},
                {"value": "25", "status": "true"}]

    for payload in payloads:
        response = requests.post(URL + "/state", json=payload)
        assert response.status_code == 400
