from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    address = models.ForeignKey(
        "Address", on_delete=models.CASCADE, blank=True, null=True
    )
    phone = models.CharField(max_length=50, blank=True)
    profile_picture = models.ImageField(
        upload_to="profile_pictures/", blank=True, null=True
    )

    def __str__(self) -> str:
        return self.username


class Address(models.Model):
    city = models.CharField(max_length=100, blank=True)
    street = models.CharField(max_length=100, blank=True)
    house = models.CharField(max_length=20, blank=True)
    postal_code = models.CharField(max_length=20, blank=True)
