from factory.django import DjangoModelFactory
from rest_framework import status
from rest_framework.reverse import reverse

from applications.utils import UniqueNameMixin


class CRUDTestsMixin:
    factory: DjangoModelFactory
    list_url_name: str
    detail_url_name: str
    model: UniqueNameMixin
    creation_data: dict
    put_data: dict
    client = None
    response = None
    object_in_database = None
    list_ordering_field: str = None
    read_serializer = None

    def test_create_ok(self):
        url = reverse(self.list_url_name)

        self.response = self.client.post(url, self.creation_data, format='json', vHTTP_ACCEPT='application/json')

        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)

    def test_create_error_not_authenticated(self):
        url = reverse(self.list_url_name)
        self.client.logout()

        self.response = self.client.post(url, self.creation_data, format='json')

        self.assertEqual(self.response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_ok(self):
        existing_object = self.factory.create()
        url = reverse(self.detail_url_name, args=[existing_object.id])

        self.response = self.client.delete(url)

        self.assertEqual(self.response.status_code, status.HTTP_204_NO_CONTENT)
        result = self.model.objects.all()
        self.assertEqual(result.count(), 0)

    def test_delete_error_not_authenticated(self):
        url = reverse(self.detail_url_name, args=[1])
        self.client.logout()

        self.response = self.client.delete(url)

        self.assertEqual(self.response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_ok(self):
        url = reverse(self.list_url_name)
        how_many = 5
        self.factory.create_batch(how_many)

        self.response = self.client.get(url, vHTTP_ACCEPT='application/json')

        self.assertEqual(self.response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.response.data['count'], how_many)
        self.assertEqual(self.response.data['next'], None)
        self.assertEqual(self.response.data['previous'], None)
        self.assertEqual(len(self.response.data['results']), how_many)

    def test_list_ok_ordering_by_field(self):
        self.test_list_ok()

        if self.list_ordering_field:
            objects_in_bd = self.model.objects.all().order_by(self.list_ordering_field)
        else:
            objects_in_bd = self.model.objects.all()

        expected = self.read_serializer(objects_in_bd, many=True).data
        actual = self.response.data['results']
        self.assertEqual(actual, expected)

    def test_list_error_not_authenticated(self):
        url = reverse(self.list_url_name)
        self.client.logout()

        self.response = self.client.get(url, vHTTP_ACCEPT='application/json')

        self.assertEqual(self.response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_ok(self):
        self.object_in_database = self.factory.create()
        url = reverse(self.detail_url_name, args=[self.object_in_database.id])

        self.response = self.client.get(url, vHTTP_ACCEPT='application/json')

        self.assertEqual(self.response.status_code, status.HTTP_200_OK)

    def test_retrieve_error_not_authenticated(self):
        url = reverse(self.detail_url_name, args=[1])
        self.client.logout()

        self.response = self.client.get(url, vHTTP_ACCEPT='application/json')

        self.assertEqual(self.response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_put_ok(self):
        self.object_in_database = self.factory.create()
        url = reverse(self.detail_url_name, args=[self.object_in_database.id])

        self.response = self.client.put(url, self.put_data, format='json', vHTTP_ACCEPT='application/json')

        self.assertEqual(self.response.status_code, status.HTTP_200_OK)
        self.object_in_database = self.model.objects.get()

    def test_put_error_not_authenticated(self):
        url = reverse(self.detail_url_name, args=[1])
        self.client.logout()

        self.response = self.client.put(url, {}, format='json', vHTTP_ACCEPT='application/json')

        self.assertEqual(self.response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_patch_ok(self):
        self.object_in_database = self.factory.create()
        url = reverse(self.detail_url_name, args=[self.object_in_database.id])

        self.response = self.client.patch(url, self.put_data, format='json', vHTTP_ACCEPT='application/json')

        self.assertEqual(self.response.status_code, status.HTTP_200_OK)
        self.object_in_database = self.model.objects.get()

    def test_patch_error_not_authenticated(self):
        url = reverse(self.detail_url_name, args=[1])
        self.client.logout()

        self.response = self.client.patch(url, {}, format='json', vHTTP_ACCEPT='application/json')

        self.assertEqual(self.response.status_code, status.HTTP_401_UNAUTHORIZED)

    def list_filtering_tester(self, filtering_field, value_to_filter, is_nested_resource=False):
        self.factory.create_batch(10)
        self.factory.create_batch(5, **{filtering_field: value_to_filter})
        value_to_filter = value_to_filter.pk if is_nested_resource else value_to_filter
        url = reverse(self.list_url_name)
        url = '{}?{}={}'.format(url, filtering_field, value_to_filter)

        self.response = self.client.get(url, vHTTP_ACCEPT='application/json')

        self.assertEqual(self.response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.response.data['count'], 5)
        self.assertEqual(self.response.data['next'], None)
        self.assertEqual(self.response.data['previous'], None)
        self.assertEqual(len(self.response.data['results']), 5)
