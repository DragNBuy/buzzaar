from django.db import models


class ProductCategory(models.Model):
    category = models.CharField(max_length=40)
