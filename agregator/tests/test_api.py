from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)


def test_publish():

    event = {
        "topic": "test",
        "event_id": "1",
        "timestamp": "2024-01-01T00:00:00",
        "source": "tester",
        "payload": {}
    }

    r = client.post("/publish", json=event)

    assert r.status_code == 200


def test_stats():

    r = client.get("/stats")

    assert r.status_code == 200