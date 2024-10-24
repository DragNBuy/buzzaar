from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    city = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=50, blank=True)
    profile_picture = models.ImageField(
        upload_to="profile_pictures/", blank=True, null=True
    )

    def __str__(self) -> str:
        return self.username
