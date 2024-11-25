from rest_framework import serializers
from .models import ProductCategory


class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = [
            "id",
            "category",
        ]
        read_only_fields = ["id"]

    def create(self, validated_data):
        category = validated_data["category"]
        cat = ProductCategory.objects.filter(category=category)
        if cat.exists():
            raise serializers.ValidationError(f"Category '{category}' already exists.")
        return ProductCategory.objects.create(**validated_data)
