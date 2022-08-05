import pytest
from starlette.testclient import TestClient

from run import app


@pytest.fixture()
def client():
    yield TestClient(app)
