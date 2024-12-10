import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
def test_product_category_creation_1(api_client):
    """
    # Pass when non-existant category is created
    #"""

    response = givenUser(api_client)

    url = reverse("product_categories-list")
    data = {
        "category": "Kompiuteriai"
    }
    response = api_client.post(url, data, format="json")

    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
def test_product_category_creation_2(api_client):
    """
    # Fail when creating a category that already exists
    #"""

    response = givenUser(api_client)

    url = reverse("product_categories-list")
    data = {
        "category": "Kompiuteriai"
    }
    response = api_client.post(url, data, format="json")
    assert response.status_code == status.HTTP_201_CREATED

    response = api_client.post(url, data, format="json")
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def givenUser(api_client):
    register_url = reverse("rest_register")
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
    api_client.post(register_url, data, format="json")

    login_url = reverse("rest_login")
    login_data = {
        "email": "newuser@gmail.com",
        "password": "strong!Password123"
    }
    return api_client.post(login_url, login_data, format="json")
