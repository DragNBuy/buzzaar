from django.db import models
from users.models import CustomUser
from rest_framework import serializers


class Product(models.Model):
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    # todo: category, condition
    title = models.CharField(max_length=30)
    description = models.CharField(max_length=500)
    initial_asking_price = models.DecimalField(max_digits=8, decimal_places=2)  # todo: implement Banker's rounding
    date_created = models.DateTimeField()
    date_sold = models.DateTimeField(null=True)
    visible = models.BooleanField()
