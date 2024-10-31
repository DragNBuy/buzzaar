import pytest
from pytest_factoryboy import register
from rest_framework.test import APIClient

from .factories import CustomUserFactory

register(CustomUserFactory, "user")


@pytest.fixture
def api_client():
    """
    Returns an instance of APIClient for making API requests in tests.
    """
    return APIClient()
