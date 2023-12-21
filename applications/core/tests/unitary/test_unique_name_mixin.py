from applications.core.tests.factories.breeds_factories import BreedsFactory
from rest_framework.test import APITestCase


class UniqueNameMixinsTests(APITestCase):
    def test_to_string_ok(self):
        some_unique_name_object = BreedsFactory.build()

        object_to_string = some_unique_name_object.__str__()

        self.assertEqual(object_to_string, some_unique_name_object.name)
