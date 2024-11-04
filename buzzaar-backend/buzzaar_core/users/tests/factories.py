import factory
from django.contrib.auth import get_user_model

from ..models import Address

CustomUser = get_user_model()


class AddressFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Address

    city = factory.Faker("city")
    street = factory.Faker("street_name")
    house = factory.Faker("building_number")
    postal_code = factory.Faker("postcode")


class CustomUserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CustomUser

    username = factory.Sequence(lambda n: f"user{n}")
    email = factory.LazyAttribute(lambda obj: f"{obj.username}@gmail.com")
    password = factory.PostGenerationMethodCall("set_password", "password123")
    address = factory.SubFactory(AddressFactory)
    phone = factory.Faker("phone_number")
