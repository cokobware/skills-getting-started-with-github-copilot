import pytest

ACTIVITY = "Chess Club"
EMAIL = "removeme@mergington.edu"


def test_unregister_success(client):
    # Add participant first
    client.post(f"/activities/{ACTIVITY}/signup?email={EMAIL}")
    resp = client.delete(f"/activities/{ACTIVITY}/participants?email={EMAIL}")
    assert resp.status_code == 200
    assert f"Removed {EMAIL}" in resp.json()["message"]
    # Confirm participant is removed
    get_resp = client.get("/activities")
    assert EMAIL not in get_resp.json()[ACTIVITY]["participants"]

def test_unregister_not_found(client):
    resp = client.delete(f"/activities/{ACTIVITY}/participants?email=notfound@school.edu")
    assert resp.status_code == 404
    assert "Participant not found" in resp.json()["detail"]

def test_unregister_activity_not_found(client):
    resp = client.delete(f"/activities/UnknownActivity/participants?email={EMAIL}")
    assert resp.status_code == 404
    assert "Activity not found" in resp.json()["detail"]

def test_unregister_and_readd(client):
    # Add, remove, then re-add
    client.post(f"/activities/{ACTIVITY}/signup?email={EMAIL}")
    client.delete(f"/activities/{ACTIVITY}/participants?email={EMAIL}")
    resp = client.post(f"/activities/{ACTIVITY}/signup?email={EMAIL}")
    assert resp.status_code == 200
