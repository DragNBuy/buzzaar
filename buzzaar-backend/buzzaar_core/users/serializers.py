from dj_rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers

from .models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = "__all__"


class CustomRegisterSerializer(RegisterSerializer):
    email = serializers.EmailField(required=True)
    city = serializers.CharField(required=False)
    phone = serializers.CharField(required=False)

    def get_cleaned_data(self):
        print("CustomRegisterSerializer is being used")
        data = super().get_cleaned_data()
        if isinstance(self.initial_data, dict):
            data["email"] = self.initial_data.get("email", "")
            data["city"] = self.initial_data.get("city", "")
            data["phone"] = self.initial_data.get("phone", "")
        return data

    def save(self, request):
        user = super().save(request)
        if isinstance(self.validated_data, dict):
            user.email = self.validated_data.get("email", "")
            user.city = self.validated_data.get("city", "")
            user.phone = self.validated_data.get("phone", "")
            user.save(update_fields=["email", "city", "phone"])
        return user
