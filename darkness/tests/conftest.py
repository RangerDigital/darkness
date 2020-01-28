import pytest


@pytest.fixture()
def URL():
    # Check the port of your running container!
    return "http://127.0.0.1:5000"
