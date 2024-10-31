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


@pytest.mark.authentication
@pytest.mark.django_db
def test_user_login(api_client, user):
    """
    Test that a user can log in successfully.
    """

    url = reverse("rest_login")
    data = {"email": user.email, "password": "password123"}
    response = api_client.post(url, data, format="json")

    assert response.status_code == status.HTTP_200_OK
    assert "buzzaar_access_token" in response.cookies
    assert "buzzaar_refresh_token" in response.cookies
