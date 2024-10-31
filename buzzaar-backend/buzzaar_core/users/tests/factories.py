import factory
from django.contrib.auth import get_user_model

CustomUser = get_user_model()


class CustomUserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CustomUser

    username = factory.Sequence(lambda n: f"user{n}")
    email = factory.LazyAttribute(lambda obj: f"{obj.username}@gmail.com")
    password = factory.PostGenerationMethodCall("set_password", "password123")
    city = factory.Faker("city")
    phone = factory.Faker("phone_number")
