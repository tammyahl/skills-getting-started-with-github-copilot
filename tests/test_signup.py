"""
Tests for the POST /activities/{activity_name}/signup endpoint using the AAA pattern.
"""

import pytest


def test_signup_successful(client):
    """
    Test successful signup for an activity.
    
    AAA Pattern:
    - Arrange: Set up test data (activity name and email)
    - Act: Make POST request to signup endpoint
    - Assert: Verify 200 status and participant is added to activity
    """
    # Arrange
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"
    
    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )
    
    # Assert
    assert response.status_code == 200
    assert "Signed up" in response.json()["message"]
    assert email in response.json()["message"]
    
    # Verify participant was actually added
    activities_response = client.get("/activities")
    activities = activities_response.json()
    assert email in activities[activity_name]["participants"]


def test_signup_activity_not_found(client):
    """
    Test signup fails when activity doesn't exist.
    
    AAA Pattern:
    - Arrange: Set up invalid activity name and valid email
    - Act: Make POST request to signup endpoint
    - Assert: Verify 404 status and error message
    """
    # Arrange
    activity_name = "NonexistentActivity"
    email = "student@mergington.edu"
    
    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )
    
    # Assert
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]


def test_signup_duplicate_fails(client):
    """
    Test signup fails when student is already signed up.
    
    AAA Pattern:
    - Arrange: Select a participant already in an activity
    - Act: Attempt to sign up the same participant again
    - Assert: Verify 400 status and error message
    """
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"  # Already in Chess Club
    
    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )
    
    # Assert
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]


def test_signup_multiple_different_activities(client):
    """
    Test that the same student can sign up for different activities.
    
    AAA Pattern:
    - Arrange: Pick a student and two different activities
    - Act: Sign up the student for both activities
    - Assert: Verify success for both and participant is in both lists
    """
    # Arrange
    email = "versatile@mergington.edu"
    activity1 = "Chess Club"
    activity2 = "Art Club"
    
    # Act
    response1 = client.post(
        f"/activities/{activity1}/signup",
        params={"email": email}
    )
    response2 = client.post(
        f"/activities/{activity2}/signup",
        params={"email": email}
    )
    
    # Assert
    assert response1.status_code == 200
    assert response2.status_code == 200
    
    activities_response = client.get("/activities")
    activities = activities_response.json()
    assert email in activities[activity1]["participants"]
    assert email in activities[activity2]["participants"]
