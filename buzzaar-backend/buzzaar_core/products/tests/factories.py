import factory
from products.models import Product
from users.tests.factories import CustomUserFactory
from datetime import datetime


class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product

    owner = factory.SubFactory(CustomUserFactory)
    title = factory.Faker('cryptocurrency_name')
    description = factory.Faker('sentence')
    initial_asking_price = factory.Faker('pyfloat')
    date_created = factory.LazyAttribute(datetime.now)
    visible = True
