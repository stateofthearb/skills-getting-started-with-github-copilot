"""Shared test fixtures for Activities API tests.

Provides fixtures for AAA (Arrange-Act-Assert) pattern testing:
- client: Fresh TestClient instance for each test
- activity_name: Reusable test activity name
- test_email: Reusable test email address
- multiple_emails: Multiple test email addresses for parametrized tests
"""

import pytest
from fastapi.testclient import TestClient

from src.app import app


@pytest.fixture
def client():
    """Provide a fresh TestClient instance for each test.
    
    Each test gets an independent client to ensure state isolation.
    Note: The in-memory activities database persists within the test session,
    so tests should not assume a clean state unless explicitly managing it.
    """
    return TestClient(app)


@pytest.fixture
def activity_name():
    """Provide a test activity name."""
    return "Chess Club"


@pytest.fixture
def test_email():
    """Provide a test email address."""
    return "student@example.com"


@pytest.fixture
def multiple_emails():
    """Provide multiple test email addresses for parametrized tests."""
    return [
        "alice@example.com",
        "bob@example.com",
        "charlie@example.com",
    ]


@pytest.fixture
def all_activities():
    """Provide list of all activity names."""
    return [
        "Chess Club",
        "Programming Class",
        "Gym Class",
        "Basketball Team",
        "Tennis Club",
        "Art Studio",
        "Drama Club",
        "Robotics Club",
        "Debate Team",
    ]
