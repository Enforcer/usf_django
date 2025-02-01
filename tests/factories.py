import factory  # type: ignore
from django.conf import settings
from factory.django import DjangoModelFactory  # type: ignore


class UserFactory(DjangoModelFactory):  # type: ignore
    class Meta:
        model = settings.AUTH_USER_MODEL

    username = factory.Sequence(lambda n: "user%d" % n)
    email = factory.Faker("email")
    password = factory.Faker("password")


class CategoryFactory(DjangoModelFactory):  # type: ignore
    class Meta:
        model = "products.Category"

    name = factory.Faker("word")
    created_by = factory.SubFactory(UserFactory)
