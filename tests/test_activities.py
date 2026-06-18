"""
Tests for the GET /activities endpoint using the AAA (Arrange-Act-Assert) pattern.
"""

import pytest


def test_get_activities_successful_retrieval(client):
    """
    Test that GET /activities returns all activities with 200 status.
    
    AAA Pattern:
    - Arrange: TestClient is provided via fixture
    - Act: Make GET request to /activities
    - Assert: Verify 200 status and activities dict is returned
    """
    # Arrange
    # (client fixture already set up)
    
    # Act
    response = client.get("/activities")
    
    # Assert
    assert response.status_code == 200
    activities = response.json()
    assert isinstance(activities, dict)
    assert len(activities) > 0


def test_get_activities_response_structure(client):
    """
    Test that GET /activities returns activities with proper structure.
    
    AAA Pattern:
    - Arrange: TestClient is provided via fixture
    - Act: Make GET request to /activities
    - Assert: Verify each activity has required fields
    """
    # Arrange
    # (client fixture already set up)
    
    # Act
    response = client.get("/activities")
    activities = response.json()
    
    # Assert
    for activity_name, activity_data in activities.items():
        assert isinstance(activity_name, str)
        assert isinstance(activity_data, dict)
        assert "description" in activity_data
        assert "schedule" in activity_data
        assert "max_participants" in activity_data
        assert "participants" in activity_data
        assert isinstance(activity_data["participants"], list)


def test_get_activities_contains_chess_club(client):
    """
    Test that GET /activities includes the Chess Club activity.
    
    AAA Pattern:
    - Arrange: TestClient is provided via fixture
    - Act: Make GET request to /activities
    - Assert: Verify Chess Club exists in response
    """
    # Arrange
    expected_activity = "Chess Club"
    
    # Act
    response = client.get("/activities")
    activities = response.json()
    
    # Assert
    assert expected_activity in activities
    assert "Learn strategies and compete in chess tournaments" in activities[expected_activity]["description"]
