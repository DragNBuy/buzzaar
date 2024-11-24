from rest_framework import serializers

from users.models import CustomUser

from .models import Product
from datetime import datetime


class ProductSerializer(serializers.ModelSerializer):
    owner_id = serializers.IntegerField(write_only=True)
    owner = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "title",
            "description",
            "initial_asking_price",
            "date_created",
            "visible",
            "owner_id",
            "owner",
        ]
        read_only_fields = ["id", "date_created", "visible", "owner"]

    def validate_owner_id(self, value):
        try:
            return CustomUser.objects.get(pk=value)
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError(f"User with id={value} does not exist.")

    def validate_initial_asking_price(self, value):
        if value >= 10**6 or value < 0:
            raise serializers.ValidationError(
                "Price can only have 6 digits before the decimal and must be positive."
            )
        return value

    def create(self, validated_data):
        owner = validated_data.pop("owner_id")
        date = datetime.now()
        return Product.objects.create(
            owner=owner,
            date_created=date,
            visible=True,
            **validated_data
        )
