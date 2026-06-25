from fastapi.testclient import TestClient

from src.app import app

client = TestClient(app)


def test_unregister_participant_removes_the_participant():
    response = client.delete(
        "/activities/Chess Club/participants",
        params={"email": "michael@mergington.edu"},
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Removed michael@mergington.edu from Chess Club"

    activities_response = client.get("/activities")
    activity = activities_response.json()["Chess Club"]
    assert "michael@mergington.edu" not in activity["participants"]


def test_unregister_participant_returns_404_when_not_found():
    response = client.delete(
        "/activities/Chess Club/participants",
        params={"email": "missing@mergington.edu"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found"


def test_activities_endpoint_avoids_caching():
    response = client.get("/activities")

    assert response.status_code == 200
    assert response.headers["cache-control"].startswith("no-store")
