import pytest
from fastapi.testclient import TestClient
from src.app import app, activities

client = TestClient(app)


def test_root_redirects_to_static():
    """Test that root path redirects to static/index.html"""
    response = client.get("/", follow_redirects=False)
    assert response.status_code == 307
    assert "/static/index.html" in response.headers["location"]


def test_get_activities():
    """Test fetching all activities"""
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "Programming Class" in data
    assert "Gym Class" in data


def test_signup_for_activity():
    """Test signing up for an activity"""
    # Reset activities to a known state
    activities["Chess Club"]["participants"] = []
    
    response = client.post(
        "/activities/Chess%20Club/signup?email=test@example.com"
    )
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "test@example.com" in data["message"]
    
    # Verify participant was added
    assert "test@example.com" in activities["Chess Club"]["participants"]


def test_signup_duplicate_participant():
    """Test that signing up twice returns an error"""
    # Reset and add participant
    activities["Chess Club"]["participants"] = ["duplicate@example.com"]
    
    response = client.post(
        "/activities/Chess%20Club/signup?email=duplicate@example.com"
    )
    assert response.status_code == 400
    data = response.json()
    assert "already signed up" in data["detail"].lower()


def test_signup_nonexistent_activity():
    """Test signing up for non-existent activity"""
    response = client.post(
        "/activities/Nonexistent%20Club/signup?email=test@example.com"
    )
    assert response.status_code == 404
    data = response.json()
    assert "not found" in data["detail"].lower()


def test_unregister_from_activity():
    """Test unregistering from an activity"""
    # Setup: add a participant
    activities["Chess Club"]["participants"] = ["unregister@example.com"]
    
    response = client.post(
        "/activities/Chess%20Club/unregister",
        json={"email": "unregister@example.com"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "unregistered" in data["message"].lower()
    
    # Verify participant was removed
    assert "unregister@example.com" not in activities["Chess Club"]["participants"]


def test_unregister_not_registered():
    """Test unregistering when not registered"""
    activities["Chess Club"]["participants"] = []
    
    response = client.post(
        "/activities/Chess%20Club/unregister",
        json={"email": "notregistered@example.com"}
    )
    assert response.status_code == 400
    data = response.json()
    assert "not registered" in data["detail"].lower()


def test_unregister_nonexistent_activity():
    """Test unregistering from non-existent activity"""
    response = client.post(
        "/activities/Nonexistent%20Club/unregister",
        json={"email": "test@example.com"}
    )
    assert response.status_code == 404
    data = response.json()
    assert "not found" in data["detail"].lower()

