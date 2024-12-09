from enum import Enum

from django.db import models

from product_categories.models import ProductCategory
from users.models import CustomUser


class Condition(Enum):
    IN_ORIGINAL_PACKAGING = "Originalioje pakuotėje"
    NEW = "Nauja"
    USED = "Naudota"
    OTHER = "Kita"


class Product(models.Model):
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    category = models.ForeignKey(ProductCategory, null=True, on_delete=models.SET_NULL)
    condition = models.CharField(max_length=22)
    title = models.CharField(max_length=30)
    description = models.CharField(max_length=512)
    initial_asking_price = models.DecimalField(
        max_digits=8, decimal_places=2
    )  # todo: implement Banker's rounding
    date_created = models.DateTimeField()
    date_sold = models.DateTimeField(null=True)
    visible = models.BooleanField()

    def __str__(self) -> str:
        return self.title


class ProductReport(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    title = models.CharField(max_length=32)
    description = models.CharField(max_length=512)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.title
