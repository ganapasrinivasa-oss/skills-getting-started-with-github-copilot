import copy
import pytest
from fastapi.testclient import TestClient

from src import app as _app_module
from src.app import app, activities

# create client
client = TestClient(app)

original_activities = copy.deepcopy(activities)

@pytest.fixture(autouse=True)
def reset_activities():
    # restore original state before each test
    activities.clear()
    activities.update(copy.deepcopy(original_activities))
    yield


def test_get_activities():
    # Arrange: nothing special
    # Act
    resp = client.get("/activities")
    # Assert
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)
    # it should contain at least one known activity
    assert "Chess Club" in data


def test_signup_success():
    # Arrange
    email = "newstudent@mergington.edu"
    activity = "Chess Club"
    # Act
    resp = client.post(f"/activities/{activity}/signup?email={email}")
    # Assert
    assert resp.status_code == 200
    assert "Signed up" in resp.json().get("message", "")
    # verify state changed
    get_resp = client.get("/activities")
    assert email in get_resp.json()[activity]["participants"]


def test_signup_duplicate():
    email = "michael@mergington.edu"
    activity = "Chess Club"
    # first signup (already in list) should fail
    resp = client.post(f"/activities/{activity}/signup?email={email}")
    assert resp.status_code == 400


def test_signup_not_found():
    resp = client.post("/activities/NoSuchActivity/signup?email=test@example.com")
    assert resp.status_code == 404


def test_remove_participant_success():
    # ensure participant exists
    activity = "Programming Class"
    email = "emma@mergington.edu"
    resp = client.delete(f"/activities/{activity}/participants?email={email}")
    assert resp.status_code == 200
    assert "Removed" in resp.json().get("message", "")
    # verify removal
    data = client.get("/activities").json()
    assert email not in data[activity]["participants"]


def test_remove_participant_not_found():
    resp = client.delete(
        "/activities/Chess%20Club/participants?email=doesnotexist@mergington.edu"
    )
    assert resp.status_code == 404
