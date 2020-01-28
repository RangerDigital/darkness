import pytest
import requests


def test_rainbow(URL):
    response = requests.get(URL + "/state")
    old_state = response.json()

    response = requests.post(URL + "/animations/rainbow")

    assert response.status_code == 200

    response = requests.get(URL + "/state")
    new_state = response.json()

    assert old_state == new_state


def test_rainbow_params(URL):
    response = requests.post(URL + "/animations/rainbow",
                             params={"duration": 2})

    assert response.status_code == 200


def test_rainbow_invalid_params(URL):
    response = requests.post(URL + "/animations/rainbow",
                             params={"duration": "hello", "hue": -45})

    assert response.status_code == 400


def test_blink(URL):
    response = requests.post(URL + "/animations/blink")

    assert response.status_code == 200


def test_blink_params(URL):
    response = requests.post(URL + "/animations/blink", params={"count": 2, "hue": 75})

    assert response.status_code == 200


def test_blink_invalid_params(URL):
    response = requests.post(URL + "/animations/blink",
                             params={"count": -3, "hue": "Hello"})

    assert response.status_code == 400
