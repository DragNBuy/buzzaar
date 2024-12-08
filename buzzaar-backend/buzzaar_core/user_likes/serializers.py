from rest_framework import serializers

from .models import UserLike
from users.models import CustomUser
from products.models import Product


class UserLikeSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all())
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())

    class Meta:
        model = UserLike
        fields = [
            "id",
            "user",
            "product"
        ]
        read_only_fields = ["id", "user", "product"]

    def validate_user_id(self, value):
        try:
            return CustomUser.objects.get(pk=value)
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError(
                f"User with id={value} does not exist."
            )

    def validate_product_id(self, value):
        try:
            return Product.objects.get(pk=value)
        except Product.DoesNotExist:
            raise serializers.ValidationError(
                f"Product with id={value} does not exist."
            )

    def create(self, validated_data):
        user = validated_data["user"]
        product = validated_data["product"]

        like = UserLike.objects.filter(user=user, product=product)
        if like.exists():
            raise serializers.ValidationError(
                f"User id={user.id} already likes product id={product.id}"
            )
        return UserLike.objects.create(
            user=user,
            product=product
        )
