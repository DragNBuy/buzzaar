from datetime import datetime

from rest_framework import serializers

from product_categories.models import ProductCategory
from users.models import CustomUser

from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    owner_id = serializers.IntegerField(write_only=True)
    owner = serializers.StringRelatedField(read_only=True)

    category_id = serializers.IntegerField(write_only=True)
    category = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "title",
            "description",
            "category_id",
            "category",
            "condition",
            "initial_asking_price",
            "date_created",
            "visible",
            "owner",
        ]
        read_only_fields = ["id", "date_created", "visible", "owner", "category"]

    def validate_category_id(self, value):
        try:
            return ProductCategory.objects.get(pk=value)
        except ProductCategory.DoesNotExist:
            raise serializers.ValidationError(
                f"Product with id={value} does not exist."
            )

    def validate_initial_asking_price(self, value):
        if value >= 10**6 or value < 0:
            raise serializers.ValidationError(
                "Price can only have 6 digits before the decimal and must be positive."
            )
        return value

    def create(self, validated_data):
        owner = self.context["request"].user
        category = validated_data.pop("category_id")
        date = datetime.now()
        return Product.objects.create(
            owner=owner,
            category=category,
            date_created=date,
            visible=True,
            **validated_data,
        )
