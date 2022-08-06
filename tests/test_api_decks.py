from starlette.testclient import TestClient


def test_without_etl(test_client: TestClient):
    response = test_client.get("/decks")
    assert response.status_code == 404
    assert response.json() == {'detail': 'ETL run not found or not completed'}
