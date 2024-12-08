from django.db import models
from users.models import CustomUser
from products.models import Product


class UserLike(models.Model):
    user = models.ForeignKey(CustomUser, null=True, on_delete=models.SET_NULL)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
