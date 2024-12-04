from datetime import datetime

from rest_framework import serializers

from product_categories.models import ProductCategory

from .models import Product, ProductPicture


class ProductPictureSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductPicture
        fields = ["id", "product", "image", "uploaded_at"]
        read_only_fields = ["id", "uploaded_at"]

    def validate_image(self, value):
        if value.size > 10 * 1024 * 1024:
            raise serializers.ValidationError("Image size must not exceed 5 MB.")

        valid_content_types = ["image/jpeg", "image/png", "image/jpg"]
        content_type = value.file.content_type
        if content_type not in valid_content_types:
            raise serializers.ValidationError(
                "Invalid file type. Only JPEG, PNG, and JPG are allowed."
            )
        return value


class ProductSerializer(serializers.ModelSerializer):
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
            "pictures",
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
