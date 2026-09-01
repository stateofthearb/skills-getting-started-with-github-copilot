"""Comprehensive test suite for Activities API using AAA (Arrange-Act-Assert) pattern.

Tests cover all endpoints with happy paths and error scenarios:
- GET /activities
- POST /activities/{activity_name}/signup
- DELETE /activities/{activity_name}/participants/{email}
"""

import pytest


class TestGetActivities:
    """Tests for GET /activities endpoint."""

    def test_get_activities_returns_200(self, client):
        """Verify GET /activities returns 200 status code."""
        # Arrange: No setup needed
        
        # Act
        response = client.get("/activities")
        
        # Assert
        assert response.status_code == 200

    def test_get_activities_returns_all_activities(self, client):
        """Verify GET /activities returns all activities."""
        # Arrange
        expected_activities = {
            "Chess Club", "Programming Class", "Gym Class", "Basketball Team",
            "Tennis Club", "Art Studio", "Drama Club", "Robotics Club", "Debate Team"
        }
        
        # Act
        response = client.get("/activities")
        activities_data = response.json()
        
        # Assert
        assert set(activities_data.keys()) == expected_activities

    def test_get_activities_returns_correct_structure(self, client):
        """Verify GET /activities response contains required fields."""
        # Arrange
        required_fields = {"description", "schedule", "max_participants", "participants"}
        
        # Act
        response = client.get("/activities")
        activities_data = response.json()
        
        # Assert
        for activity_name, activity_data in activities_data.items():
            assert set(activity_data.keys()) == required_fields
            assert isinstance(activity_data["participants"], list)
            assert isinstance(activity_data["max_participants"], int)


class TestSignupForActivity:
    """Tests for POST /activities/{activity_name}/signup endpoint."""

    def test_signup_returns_200_on_success(self, client, activity_name, test_email):
        """Verify successful signup returns 200 status code."""
        # Arrange: Use fixtures to prepare test data
        
        # Act
        response = client.post(f"/activities/{activity_name}/signup?email={test_email}")
        
        # Assert
        assert response.status_code == 200

    def test_signup_adds_email_to_participants(self, client, activity_name, test_email):
        """Verify email is added to activity participants after signup."""
        # Arrange
        
        # Act
        client.post(f"/activities/{activity_name}/signup?email={test_email}")
        activities = client.get("/activities").json()
        
        # Assert
        assert test_email in activities[activity_name]["participants"]

    def test_signup_returns_200_message(self, client, activity_name, test_email):
        """Verify signup response contains success message."""
        # Arrange
        
        # Act
        response = client.post(f"/activities/{activity_name}/signup?email={test_email}")
        response_data = response.json()
        
        # Assert
        assert "message" in response_data
        assert test_email in response_data["message"]
        assert activity_name in response_data["message"]

    def test_signup_returns_404_for_nonexistent_activity(self, client, test_email):
        """Verify signup returns 404 for nonexistent activity."""
        # Arrange
        nonexistent_activity = "Nonexistent Club"
        
        # Act
        response = client.post(f"/activities/{nonexistent_activity}/signup?email={test_email}")
        
        # Assert
        assert response.status_code == 404
        assert "Activity not found" in response.json()["detail"]

    def test_signup_returns_400_for_duplicate_signup(self, client, activity_name):
        """Verify signup returns 400 when student is already signed up."""
        # Arrange
        email = "michael@mergington.edu"  # Already in Chess Club
        
        # Act
        response = client.post(f"/activities/{activity_name}/signup?email={email}")
        
        # Assert
        assert response.status_code == 400
        assert "already signed up" in response.json()["detail"]

    @pytest.mark.parametrize("activity", [
        "Chess Club", "Programming Class", "Gym Class", "Basketball Team",
        "Tennis Club", "Art Studio", "Drama Club", "Robotics Club", "Debate Team"
    ])
    def test_signup_works_for_all_activities(self, client, activity):
        """Verify signup works for all activities (parametrized test)."""
        # Arrange
        test_email = "parametrized@example.com"
        
        # Act
        response = client.post(f"/activities/{activity}/signup?email={test_email}")
        
        # Assert
        assert response.status_code == 200


class TestUnregisterParticipant:
    """Tests for DELETE /activities/{activity_name}/participants/{email} endpoint."""

    def test_unregister_returns_200_on_success(self, client, activity_name, test_email):
        """Verify successful unregister returns 200 status code."""
        # Arrange
        client.post(f"/activities/{activity_name}/signup?email={test_email}")
        
        # Act
        response = client.delete(f"/activities/{activity_name}/participants/{test_email}")
        
        # Assert
        assert response.status_code == 200

    def test_unregister_removes_email_from_participants(self, client, activity_name, test_email):
        """Verify email is removed from participants after unregister."""
        # Arrange
        client.post(f"/activities/{activity_name}/signup?email={test_email}")
        
        # Act
        client.delete(f"/activities/{activity_name}/participants/{test_email}")
        activities = client.get("/activities").json()
        
        # Assert
        assert test_email not in activities[activity_name]["participants"]

    def test_unregister_returns_200_message(self, client, activity_name, test_email):
        """Verify unregister response contains success message."""
        # Arrange
        client.post(f"/activities/{activity_name}/signup?email={test_email}")
        
        # Act
        response = client.delete(f"/activities/{activity_name}/participants/{test_email}")
        response_data = response.json()
        
        # Assert
        assert "message" in response_data
        assert test_email in response_data["message"]
        assert activity_name in response_data["message"]

    def test_unregister_returns_404_for_nonexistent_participant(self, client, activity_name):
        """Verify unregister returns 404 for nonexistent participant."""
        # Arrange
        nonexistent_email = "nonexistent@example.com"
        
        # Act
        response = client.delete(f"/activities/{activity_name}/participants/{nonexistent_email}")
        
        # Assert
        assert response.status_code == 404
        assert "Participant not found" in response.json()["detail"]

    def test_unregister_returns_404_for_nonexistent_activity(self, client, test_email):
        """Verify unregister returns 404 for nonexistent activity."""
        # Arrange
        nonexistent_activity = "Nonexistent Club"
        
        # Act
        response = client.delete(f"/activities/{nonexistent_activity}/participants/{test_email}")
        
        # Assert
        assert response.status_code == 404
        assert "Activity not found" in response.json()["detail"]

    def test_unregister_participant_removes_email_from_activity(self, client, activity_name, test_email):
        """Integration test: signup, unregister, verify removal and re-delete returns 404."""
        # Arrange (Setup: sign up a student)
        signup_response = client.post(f"/activities/{activity_name}/signup?email={test_email}")
        assert signup_response.status_code == 200
        
        # Act (First delete: should succeed)
        delete_response = client.delete(f"/activities/{activity_name}/participants/{test_email}")
        assert delete_response.status_code == 200
        
        # Assert (Verify removal)
        assert test_email not in client.get("/activities").json()[activity_name]["participants"]
        
        # Act (Second delete: should fail)
        cleanup_response = client.delete(f"/activities/{activity_name}/participants/{test_email}")
        
        # Assert (Verify 404)
        assert cleanup_response.status_code == 404
