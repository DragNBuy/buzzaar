from rest_framework import serializers
from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    owner = serializers.IntegerField(source="owner.id")

    class Meta:
        model = Product
        fields = ["owner", "title", "description", "initial_asking_price", "date_created", "date_sold", "visible"]
