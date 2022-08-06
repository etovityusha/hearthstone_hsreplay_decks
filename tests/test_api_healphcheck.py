from starlette.testclient import TestClient


def test_healthcheck(test_client: TestClient):
    response = test_client.get("/healthcheck")
    assert response.status_code == 200
    assert response.json() == {'message': 'Everything is fine', 'status': 'OK'}
