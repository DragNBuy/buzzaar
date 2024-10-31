import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.authentication
@pytest.mark.django_db
def test_user_registration(api_client):
    """
    Test that a user can register successfully.
    """
    url = reverse("rest_register")
    data = {
        "email": "newuser@gmail.com",
        "username": "newuser",
        "password1": "strong!Password123",
        "password2": "strong!Password123",
        "city": "test city",
        "phone": "123456789",
    }
    response = api_client.post(url, data, format="json")

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["user"]["email"] == "newuser@gmail.com"
    assert response.data["user"]["username"] == "newuser"
