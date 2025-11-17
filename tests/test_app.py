import pytest
from fastapi.testclient import TestClient
from src.app import app, activities

client = TestClient(app)

# --- GET /activities ---
def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data

# --- POST /activities/{activity_name}/signup ---
def test_signup_for_activity():
    activity = "Chess Club"
    email = "testuser@mergington.edu"
    # Ensure not already signed up
    if email in activities[activity]["participants"]:
        activities[activity]["participants"].remove(email)
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 200
    assert email in activities[activity]["participants"]
    assert "Signed up" in response.json()["message"]

# --- POST /activities/{activity_name}/signup (already signed up) ---
def test_signup_already_signed_up():
    activity = "Chess Club"
    email = "testuser@mergington.edu"
    # Ensure already signed up
    if email not in activities[activity]["participants"]:
        activities[activity]["participants"].append(email)
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"

# --- POST /activities/{activity_name}/unregister ---
def test_unregister_from_activity():
    activity = "Chess Club"
    email = "testuser@mergington.edu"
    # Ensure already signed up
    if email not in activities[activity]["participants"]:
        activities[activity]["participants"].append(email)
    response = client.post(f"/activities/{activity}/unregister?email={email}")
    assert response.status_code == 200
    assert email not in activities[activity]["participants"]
    assert "Unregistered" in response.json()["message"]

# --- POST /activities/{activity_name}/unregister (not registered) ---
def test_unregister_not_registered():
    activity = "Chess Club"
    email = "notregistered@mergington.edu"
    # Ensure not registered
    if email in activities[activity]["participants"]:
        activities[activity]["participants"].remove(email)
    response = client.post(f"/activities/{activity}/unregister?email={email}")
    assert response.status_code == 400
    assert response.json()["detail"] == "Student not registered for this activity"
