from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient


class ProductCreationTestCase(TestCase):
    def setUp(self):
        self.valid_price = "12.3"
        self.api_client = APIClient()

    def test_productCreation1(self):
        """
        # Pass when user creates a product
        #"""
        user_id = givenRegisteredUser(self.api_client)
        givenLoggedInUser(self.api_client)
        category_id = givenCategory(self.api_client)
        products_url = reverse("products-list")
        product_data = {
            "owner_id": user_id,
            "category_id": category_id,
            "condition": "New",
            "title": "My Item",
            "description": "This is my item that i wish to sell",
            "initial_asking_price": self.valid_price,
        }
        product_response = self.api_client.post(products_url, product_data, format="json")
        assert product_response.status_code == status.HTTP_201_CREATED

    def test_productCreationFail1(self):
        """
        # Fail when price is negative
        #"""
        user_id = givenRegisteredUser(self.api_client)
        givenLoggedInUser(self.api_client)
        category_id = givenCategory(self.api_client)
        url = reverse("products-list")
        data = {
            "owner_id": user_id,
            "category_id": category_id,
            "condition": "New",
            "title": "My Item",
            "description": "This is my item that i wish to sell",
            "initial_asking_price": "-11.11",
        }
        product_response = self.api_client.post(url, data, format="json")
        assert product_response.status_code == status.HTTP_400_BAD_REQUEST

    def test_productCreationFail2(self):
        """
        # Fail when price has more than 8 digits in total
        #"""
        user_id = givenRegisteredUser(self.api_client)
        givenLoggedInUser(self.api_client)
        category_id = givenCategory(self.api_client)
        url = reverse("products-list")
        data = {
            "owner_id": user_id,
            "category_id": category_id,
            "condition": "New",
            "title": "My Item",
            "description": "This is my item that i wish to sell",
            "initial_asking_price": "12345678.11",
        }
        product_response = self.api_client.post(url, data, format="json")
        assert product_response.status_code == status.HTTP_400_BAD_REQUEST

    def test_productCreationFail3(self):
        """
        # Fail when category is not specified
        #"""
        user_id = givenRegisteredUser(self.api_client)
        givenLoggedInUser(self.api_client)
        url = reverse("products-list")
        data = {
            "owner_id": user_id,
            "condition": "New",
            "title": "My Item",
            "description": "This is my item that i wish to sell",
            "initial_asking_price": self.valid_price,
        }
        product_response = self.api_client.post(url, data, format="json")
        assert product_response.status_code == status.HTTP_400_BAD_REQUEST

    def test_productCreationFail4(self):
        """
        # Fail when condition is not specified
        #"""
        user_id = givenRegisteredUser(self.api_client)
        givenLoggedInUser(self.api_client)
        category_id = givenCategory(self.api_client)
        givenLoggedInUser(self.api_client)
        url = reverse("products-list")
        data = {
            "owner_id": user_id,
            "category_id": category_id,
            "title": "My Item",
            "description": "This is my item that i wish to sell",
            "initial_asking_price": self.valid_price,
        }
        product_response = self.api_client.post(url, data, format="json")
        assert product_response.status_code == status.HTTP_400_BAD_REQUEST


def givenRegisteredUser(api_client):
    register_url = reverse("rest_register")
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
    response = api_client.post(register_url, data, format="json")
    return response.data["user"]["id"]


def givenLoggedInUser(api_client):
    login_url = reverse("rest_login")
    login_data = {
        "email": "newuser@gmail.com",
        "password": "strong!Password123"
    }
    return api_client.post(login_url, login_data, format="json")


def givenCategory(api_client):
    categories_url = reverse("product_categories-list")
    category_data = {
        "category": "Kompiuteriai"
    }
    response = api_client.post(categories_url, category_data, format="json")
    return response.data["id"]
