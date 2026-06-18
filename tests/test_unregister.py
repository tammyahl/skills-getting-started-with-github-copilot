"""
Tests for the DELETE /activities/{activity_name}/participants endpoint using the AAA pattern.
"""

import pytest


def test_unregister_successful(client):
    """
    Test successful unregistration from an activity.
    
    AAA Pattern:
    - Arrange: Select an activity and participant to remove
    - Act: Make DELETE request to unregister endpoint
    - Assert: Verify 200 status and participant is removed from activity
    """
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"  # Already in Chess Club
    
    # Act
    response = client.delete(
        f"/activities/{activity_name}/participants",
        params={"email": email}
    )
    
    # Assert
    assert response.status_code == 200
    assert "Unregistered" in response.json()["message"]
    assert email in response.json()["message"]
    
    # Verify participant was actually removed
    activities_response = client.get("/activities")
    activities = activities_response.json()
    assert email not in activities[activity_name]["participants"]


def test_unregister_activity_not_found(client):
    """
    Test unregister fails when activity doesn't exist.
    
    AAA Pattern:
    - Arrange: Set up invalid activity name and valid email
    - Act: Make DELETE request to unregister endpoint
    - Assert: Verify 404 status and error message
    """
    # Arrange
    activity_name = "NonexistentActivity"
    email = "student@mergington.edu"
    
    # Act
    response = client.delete(
        f"/activities/{activity_name}/participants",
        params={"email": email}
    )
    
    # Assert
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]


def test_unregister_participant_not_found(client):
    """
    Test unregister fails when participant is not in activity.
    
    AAA Pattern:
    - Arrange: Select an activity and an email not in that activity
    - Act: Attempt to unregister the participant
    - Assert: Verify 404 status and error message
    """
    # Arrange
    activity_name = "Chess Club"
    email = "notamember@mergington.edu"
    
    # Act
    response = client.delete(
        f"/activities/{activity_name}/participants",
        params={"email": email}
    )
    
    # Assert
    assert response.status_code == 404
    assert "Participant not found" in response.json()["detail"]


def test_unregister_then_signup_again(client):
    """
    Test that a student can unregister and then sign up again.
    
    AAA Pattern:
    - Arrange: Select an activity and participant
    - Act: Unregister, then sign up again
    - Assert: Verify both operations succeed and participant is in final list
    """
    # Arrange
    activity_name = "Art Club"
    email = "flexible@mergington.edu"
    
    # Act & Assert - First signup
    signup_response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )
    assert signup_response.status_code == 200
    
    # Act & Assert - Unregister
    unregister_response = client.delete(
        f"/activities/{activity_name}/participants",
        params={"email": email}
    )
    assert unregister_response.status_code == 200
    
    # Verify participant was removed
    activities_response = client.get("/activities")
    activities = activities_response.json()
    assert email not in activities[activity_name]["participants"]
    
    # Act & Assert - Sign up again
    signup_again_response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )
    assert signup_again_response.status_code == 200
    
    # Verify participant is back in the list
    activities_response = client.get("/activities")
    activities = activities_response.json()
    assert email in activities[activity_name]["participants"]
