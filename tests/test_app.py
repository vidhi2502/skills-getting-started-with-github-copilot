import copy

from fastapi.testclient import TestClient

from src.app import activities, app

initial_activities = copy.deepcopy(activities)
client = TestClient(app)


def reset_activities():
    activities.clear()
    activities.update(copy.deepcopy(initial_activities))


def test_get_activities():
    reset_activities()

    response = client.get("/activities")

    assert response.status_code == 200

    data = response.json()
    assert "Chess Club" in data
    assert data["Chess Club"]["max_participants"] == 12
    assert isinstance(data["Chess Club"]["participants"], list)


def test_signup_for_activity():
    reset_activities()

    response = client.post(
        "/activities/Chess%20Club/signup?email=test@example.com"
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Signed up test@example.com for Chess Club"
    assert "test@example.com" in activities["Chess Club"]["participants"]


def test_signup_invalid_activity():
    reset_activities()

    response = client.post(
        "/activities/Nonexistent%20Club/signup?email=test@example.com"
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_remove_participant():
    reset_activities()

    response = client.delete(
        "/activities/Chess%20Club/signup?email=michael@mergington.edu"
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Removed michael@mergington.edu from Chess Club"
    assert "michael@mergington.edu" not in activities["Chess Club"]["participants"]


def test_remove_nonexistent_participant():
    reset_activities()

    response = client.delete(
        "/activities/Chess%20Club/signup?email=missing@example.com"
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found"
