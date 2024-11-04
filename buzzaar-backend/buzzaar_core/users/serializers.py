from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import LoginSerializer
from rest_framework import serializers

from .models import Address, CustomUser


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ["city", "street", "house", "postal_code"]


class CustomUserSerializer(serializers.ModelSerializer):
    address = AddressSerializer(read_only=True)

    class Meta:
        model = CustomUser
        fields = "__all__"


class CustomRegisterSerializer(RegisterSerializer):
    email = serializers.EmailField(required=True)
    city = serializers.CharField(required=False)
    street = serializers.CharField(required=False)
    house = serializers.CharField(required=False)
    postal_code = serializers.CharField(required=False)
    phone = serializers.CharField(required=False)

    def get_cleaned_data(self):
        data = super().get_cleaned_data()
        if isinstance(self.initial_data, dict):
            data["email"] = self.initial_data.get("email", "")
            data["city"] = self.initial_data.get("city", "")
            data["street"] = self.initial_data.get("street", "")
            data["house"] = self.initial_data.get("house", "")
            data["postal_code"] = self.initial_data.get("postal_code", "")
            data["phone"] = self.initial_data.get("phone", "")
        return data

    def save(self, request):
        user = super().save(request)
        self.user = user

        if isinstance(self.validated_data, dict):
            address_data = {
                "city": self.validated_data.get("city", ""),
                "street": self.validated_data.get("street", ""),
                "house": self.validated_data.get("house", ""),
                "postal_code": self.validated_data.get("postal_code", ""),
            }

            if any(address_data.values()):
                address = Address.objects.create(**address_data)
                user.address = address

            user.email = self.validated_data.get("email", "")
            user.phone = self.validated_data.get("phone", "")
            user.save(update_fields=["email", "phone", "address"])

        return user


class CustomLoginSerializer(LoginSerializer):
    username = None
    email = serializers.EmailField(required=True)
    password = serializers.CharField(
        style={"input_type": "password"}, trim_whitespace=False
    )
