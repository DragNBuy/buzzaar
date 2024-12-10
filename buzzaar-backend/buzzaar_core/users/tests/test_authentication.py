from urllib.parse import parse_qs, urlparse

import pytest
from django.core import mail
from django.urls import reverse
from rest_framework import status


@pytest.mark.authentication
@pytest.mark.django_db
def test_user_registration(api_client):
    """
    Test that a user can register successfully and email confirmation is required.
    """
    url = reverse("rest_register")
    data = validUserData()
    response = api_client.post(url, data, format="json")

    assert response.status_code == status.HTTP_201_CREATED

    login_url = reverse("rest_login")
    login_data = {"email": "newuser@gmail.com", "password": "strong!Password123"}
    login_response = api_client.post(login_url, login_data, format="json")

    assert login_response.status_code == status.HTTP_200_OK
    assert "buzzaar_access_token" in login_response.cookies
    assert "buzzaar_refresh_token" in login_response.cookies


@pytest.mark.authentication
@pytest.mark.django_db
def test_user_registration_fail1(api_client):
    """
    Fail when first name is not given
    """
    url = reverse("rest_register")
    data = validUserData()
    data.pop("first_name")
    response = api_client.post(url, data, format="json")

    assert response.status_code == status.HTTP_400_BAD_REQUEST

    login_url = reverse("rest_login")
    login_data = {"email": "newuser@gmail.com", "password": "strong!Password123"}
    login_response = api_client.post(login_url, login_data, format="json")

    assert login_response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.authentication
@pytest.mark.django_db
def test_user_registration_fail2(api_client):
    """
    Fail when last name is not given
    """
    url = reverse("rest_register")
    data = validUserData()
    data.pop("last_name")
    response = api_client.post(url, data, format="json")

    assert response.status_code == status.HTTP_400_BAD_REQUEST

    login_url = reverse("rest_login")
    login_data = {"email": "newuser@gmail.com", "password": "strong!Password123"}
    login_response = api_client.post(login_url, login_data, format="json")

    assert login_response.status_code == status.HTTP_400_BAD_REQUEST


def validUserData():
    data = {
        "email": "newuser@gmail.com",
        "username": "newuser",
        "first_name": "New",
        "last_name": "User",
        "password1": "strong!Password123",
        "password2": "strong!Password123",
        "phone": "123456789",
        "city": "test city",
        "street": "test street",
        "house": "123",
        "postal_code": "123456",
    }
    return data
