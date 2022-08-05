from starlette.testclient import TestClient


def test_healthcheck(client: TestClient):
    response = client.get("/healthcheck")
    assert response.status_code == 200
    assert response.json() == {'message': 'Everything is fine', 'status': 'OK'}
