import pytest
from django.urls import reverse
from rest_framework import status

from products.views import ProductViewSet


@pytest.mark.django_db
def test_product_creation_1(api_client):
    """
    # Pass when user creates a product
    #"""

    response = givenUser(api_client)

    user_id = response.json().get("user").get("id")
    url = reverse("products-list")
    data = {
        "owner_id": user_id,
        "title": "My Item",
        "description": "This is my item that i wish to sell",
        "initial_asking_price": "12.3",
    }
    response = api_client.post(url, data, format="json")

    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
def test_product_creation_fail_1(api_client):
    """
    # Fail when product price exceeds 6 digits before floating point
    #"""

    response = givenUser(api_client)

    user_id = response.json().get("user").get("id")
    url = reverse("products-list")
    data = {
        "owner_id": user_id,
        "title": "My Item",
        "description": "This is my item that i wish to sell",
        "initial_asking_price": "1234567.3",
    }
    response = api_client.post(url, data, format="json")

    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_product_creation_fail_2(api_client):
    """
    # Fail when product is created by non-existing user
    #"""

    url = reverse("products-list")
    data = {
        "owner_id": "999",
        "title": "My Item",
        "description": "This is my item that i wish to sell",
        "intitial_asking_price": "12.3",
    }
    response = api_client.post(url, data, format="json")

    assert response.status_code == status.HTTP_424_FAILED_DEPENDENCY


def givenUser(api_client):
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
    return api_client.post(url, data, format="json")
