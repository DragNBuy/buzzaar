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
    data = {
        "email": "newuser@gmail.com",
        "username": "newuser",
        "password1": "strong!Password123",
        "password2": "strong!Password123",
        "phone": "123456789",
        "city": "test city",
        "street": "test street",
        "house": "123",
        "postal_code": "123456",
    }
    response = api_client.post(url, data, format="json")

    assert response.status_code == status.HTTP_201_CREATED
    assert "detail" in response.data
    assert response.data["detail"] == "Verification e-mail sent."

    assert len(mail.outbox) == 1
    confirmation_email = mail.outbox[0]
    assert "Confirm Your Email Address" in confirmation_email.subject

    confirmation_url = None
    for line in confirmation_email.body.splitlines():
        if "http" in line:
            confirmation_url = line.strip()
            break

    assert confirmation_url is not None, "No confirmation URL found in email"

    parsed_url = urlparse(confirmation_url)
    query_params = parse_qs(parsed_url.query)
    confirmation_key = query_params.get("key", [None])[0]

    assert confirmation_key is not None, "No confirmation key found in URL"

    verify_url = reverse("rest_verify_email")
    response = api_client.post(verify_url, data={"key": confirmation_key})

    assert response.status_code == status.HTTP_200_OK
    assert response.data["detail"] == "ok"

    login_url = reverse("rest_login")
    login_data = {"email": "newuser@gmail.com", "password": "strong!Password123"}
    login_response = api_client.post(login_url, login_data, format="json")

    assert login_response.status_code == status.HTTP_200_OK
    assert "buzzaar_access_token" in login_response.cookies
    assert "buzzaar_refresh_token" in login_response.cookies
