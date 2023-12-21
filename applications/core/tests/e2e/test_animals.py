from applications.core.serializers.animals_serializers import AnimalReadSerializer
from applications.core.tests.factories.animals_factories import AnimalsFactory
from applications.core.tests.factories.owners_factories import OwnersFactory
from applications.core.tests.factories.weights_registries_factories import WeightsRegistriesFactory
from datetime import timedelta
from dateutil import parser
from dateutil.relativedelta import relativedelta
from django.utils.timezone import now
from rest_framework import status
from rest_framework.reverse import reverse
from unittest.mock import PropertyMock, patch

from applications.core.models import Animal, DicoseCategory
from applications.core.tests.e2e.crud_tests_mixin import CRUDTestsMixin
from applications.core.tests.e2e.drf_tenants import DrfTenantsTestCase


class AnimalsTests(CRUDTestsMixin, DrfTenantsTestCase):
    factory = AnimalsFactory
    list_url_name = 'animals-list'
    detail_url_name = 'animals-detail'
    model = Animal
    read_serializer = AnimalReadSerializer

    def setUp(self):
        super().setUp()
        self.dicose = DicoseCategory.objects.all().first()
        self.owner = OwnersFactory.create()
        self.creation_data = {'earring_number': '123', 'owner': self.owner.pk,
                              'age_in_months': self.dicose.minimum_age_in_months}
        self.put_data = {'earring_number': '987', 'owner': self.owner.pk, 'sex': self.dicose.sex,
                         'age_in_months': self.dicose.minimum_age_in_months}

    def test_create_error_negative_age(self):
        url = reverse(self.list_url_name)
        self.creation_data['age_in_months'] = -10

        self.response = self.client.post(url, self.creation_data, format='json', vHTTP_ACCEPT='application/json')

        self.assertEqual(self.response.status_code, status.HTTP_400_BAD_REQUEST)
        error_message = 'Birth date cannot be in the future.'
        self.assertEqual(str(self.response.data['birth_date'][0]), error_message)

    def test_retrieve_ok(self):
        super().test_retrieve_ok()

        response_data = self.response.data
        self.assertEqual(response_data['earring_number'], self.object_in_database.earring_number)
        self.assertEqual(response_data['animal_state'], self.object_in_database.animal_state)
        self.assertEqual(response_data['age_in_months'], self.object_in_database.age_in_months)
        self.assertEqual(response_data['dicose_category']['name'], self.object_in_database.dicose_category.name)
        self.assertEqual(response_data['owner']['id'], self.object_in_database.owner.id)
        self.assertEqual(response_data['owner']['name'], self.object_in_database.owner.name)
        self.assertEqual(response_data['species'], self.object_in_database.species)
        self.assertEqual(response_data['breed'], None)
        self.assertEqual(response_data['tag'], None)

    def test_weights_returns_the_latest_five_weights_ordered_by_date_descending(self):
        date1 = now() - timedelta(days=10)
        date2 = now() - timedelta(days=1)
        date3 = now() - timedelta(days=20)
        date4 = now() - timedelta(days=30)
        date5 = now() - timedelta(days=40)
        date6 = now() - timedelta(days=100)
        animal = self.factory.create()
        WeightsRegistriesFactory(animal=animal, date=date1)
        WeightsRegistriesFactory(animal=animal, date=date2)
        WeightsRegistriesFactory(animal=animal, date=date3)
        WeightsRegistriesFactory(animal=animal, date=date4)
        WeightsRegistriesFactory(animal=animal, date=date5)
        WeightsRegistriesFactory(animal=animal, date=date6)
        url = reverse('animals-weights')

        response = self.client.get(url)

        animal_data = response.data['results']
        self.assertEqual(len(animal_data), 1)
        self.assertEqual(animal_data[0]['earring_number'], animal.earring_number)
        animal_weights = animal_data[0]['weights']
        self.assertEqual(len(animal_weights), 5)
        self.assertEqual(parser.parse(animal_weights[0]['date']).date(), date2.date())
        self.assertEqual(parser.parse(animal_weights[1]['date']).date(), date1.date())
        self.assertEqual(parser.parse(animal_weights[2]['date']).date(), date3.date())
        self.assertEqual(parser.parse(animal_weights[3]['date']).date(), date4.date())
        self.assertEqual(parser.parse(animal_weights[4]['date']).date(), date5.date())

    def test_batch_delete(self):
        animal1 = self.factory.create()
        animal2 = self.factory.create()
        animal3 = self.factory.create()
        fake_animal = '123'
        url = reverse('animals-batch-delete')
        deletion_data = {'earring_numbers': [animal1.earring_number,
                                             animal2.earring_number, animal3.earring_number, fake_animal]}

        response = self.client.post(url, deletion_data, format='json', vHTTP_ACCEPT='application/json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        delete_data = response.data
        self.assertEqual(delete_data['deleted_count'], 3)
        self.assertEqual(delete_data['failed_count'], 1)
        self.assertEqual(len(delete_data['failed_animals']), 1)
        self.assertEqual(delete_data['failed_animals'][0]['earring_number'], fake_animal)

    def test_dicose_category_automatic_update(self):
        eleven_months_ago = now() - relativedelta(months=11)
        animal = self.factory.create(birth_date=eleven_months_ago)
        self.assertEqual(animal.age_in_months, 11)
        self.assertEqual(animal.dicose_category, DicoseCategory.objects.get(name='Veal'))

        property_to_mock = 'applications.core.models.animal.Animal.age_in_months'
        with patch(property_to_mock, new_callable=PropertyMock) as mock_animal_age:
            mock_animal_age.return_value = 12
            self.assertEqual(animal.age_in_months, 12)
            self.assertEqual(animal.dicose_category, DicoseCategory.objects.get(name='Heifer from 1 to 2'))
