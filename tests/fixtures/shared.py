import pytest

from rest_framework.test import APIClient


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user_data():
    return {
        "name": "Test User",
        "email": "testuser@example.com",
        "password": "testpassword",
    }
