"""
Pytest configuration and shared fixtures for the test suite.
"""

import pytest
from fastapi.testclient import TestClient
from src.app import app


@pytest.fixture
def client():
    """
    Fixture that provides a TestClient instance for making requests to the FastAPI app.
    
    Yields:
        TestClient: A test client for the FastAPI application.
    """
    return TestClient(app)
