import pytest

ACTIVITY = "Chess Club"
EMAIL = "newstudent@mergington.edu"


def test_signup_success(client):
    resp = client.post(f"/activities/{ACTIVITY}/signup?email={EMAIL}")
    assert resp.status_code == 200
    assert f"Signed up {EMAIL}" in resp.json()["message"]
    # Confirm participant is added
    get_resp = client.get("/activities")
    assert EMAIL in get_resp.json()[ACTIVITY]["participants"]

def test_signup_duplicate(client):
    # First signup
    client.post(f"/activities/{ACTIVITY}/signup?email={EMAIL}")
    # Duplicate
    resp = client.post(f"/activities/{ACTIVITY}/signup?email={EMAIL}")
    assert resp.status_code == 400
    assert "already signed up" in resp.json()["detail"]

def test_signup_activity_not_found(client):
    resp = client.post("/activities/UnknownActivity/signup?email=someone@school.edu")
    assert resp.status_code == 404
    assert "Activity not found" in resp.json()["detail"]

def test_signup_activity_full(client):
    # Fill up activity
    full_activity = "Debate Team"
    for i in range(12):
        client.post(f"/activities/{full_activity}/signup?email=student{i}@school.edu")
    resp = client.post(f"/activities/{full_activity}/signup?email=extrastudent@school.edu")
    assert resp.status_code == 400
    assert "Activity is full" in resp.json()["detail"]
