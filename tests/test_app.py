import pytest
from src.app import app


@pytest.fixture
def client():
    """Creates a test client — a fake browser that hits your app without running the server."""
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_health_check(client):
    """Test: Does the /health endpoint return 200 and 'healthy'?"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json()["status"] == "healthy"


def test_get_tasks_empty(client):
    """Test: When no tasks exist, does /api/tasks return an empty list?"""
    response = client.get("/api/tasks")
    assert response.status_code == 200
    assert response.get_json()["tasks"] == []


def test_create_task(client):
    """Test: Can we create a task with a title?"""
    response = client.post(
        "/api/tasks",
        json={"title": "Learn DevOps"},
    )
    assert response.status_code == 201
    data = response.get_json()
    assert data["title"] == "Learn DevOps"
    assert data["done"] is False
    assert data["id"] == 1


def test_create_task_missing_title(client):
    """Test: Does the API reject a task without a title?"""
    response = client.post(
        "/api/tasks",
        json={},
    )
    assert response.status_code == 400
    assert "error" in response.get_json()


def test_update_task(client):
    """Test: Can we mark a task as done?"""
    client.post("/api/tasks", json={"title": "Test task"})
    response = client.put("/api/tasks/1")
    assert response.status_code == 200
    assert response.get_json()["done"] is True


def test_update_task_not_found(client):
    """Test: Does updating a non-existent task return 404?"""
    response = client.put("/api/tasks/999")
    assert response.status_code == 404

def test_get_version(client):
    """Version endpoint should return current version."""
    response = client.get("/api/version")
    assert response.status_code == 200
    assert "version" in response.get_json()