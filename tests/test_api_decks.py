from starlette.testclient import TestClient


def test_without_etl(client: TestClient):
    response = client.get("/decks")
    assert response.status_code == 404
    assert response.json() == {'detail': 'ETL run not found or not completed'}
