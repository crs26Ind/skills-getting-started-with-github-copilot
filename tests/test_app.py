import pytest
from fastapi.testclient import TestClient
from src.app import app, activities

client = TestClient(app)

@pytest.fixture(autouse=True)
def reset_activities():
    # Arrange: Reset the in-memory activities before each test
    for activity in activities.values():
        activity['participants'].clear()


def test_get_activities():
    # Arrange: Ensure activities dict is not empty
    # Act
    response = client.get("/activities")
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert all('participants' in v for v in data.values())


def test_signup_success():
    # Arrange
    activity_name = next(iter(activities))
    email = "student1@mergington.edu"
    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={email}")
    # Assert
    assert response.status_code == 200
    assert email in activities[activity_name]['participants']


def test_signup_duplicate():
    # Arrange
    activity_name = next(iter(activities))
    email = "student2@mergington.edu"
    activities[activity_name]['participants'].append(email)
    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={email}")
    # Assert
    assert response.status_code == 400
    assert response.json()['detail'] == "Student already signed up for this activity"


def test_signup_nonexistent_activity():
    # Arrange
    activity_name = "nonexistent"
    email = "student3@mergington.edu"
    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={email}")
    # Assert
    assert response.status_code == 404
    assert response.json()['detail'] == "Activity not found"
