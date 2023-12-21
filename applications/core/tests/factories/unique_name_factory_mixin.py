import factory
from factory.django import DjangoModelFactory


class UniqueNameFactoryMixin(DjangoModelFactory):
    class Meta:
        django_get_or_create = ['name']

    name = factory.Faker('pystr')
