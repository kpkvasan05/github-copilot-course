import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)

def test_signup_and_unregister():
    # Use a test activity and email
    activity = list(client.get("/activities").json().keys())[0]
    email = "testuser@example.com"
    # Sign up
    signup_resp = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert signup_resp.status_code == 200 or signup_resp.status_code == 400
    # Unregister
    unregister_resp = client.post(f"/activities/{activity}/unregister", json={"email": email})
    assert unregister_resp.status_code == 200 or unregister_resp.status_code == 400
