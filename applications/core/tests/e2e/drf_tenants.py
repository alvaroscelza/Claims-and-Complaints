from django.contrib.auth import get_user_model
from django_tenants.test.cases import TenantTestCase
from django_tenants.test.client import TenantClient
from rest_framework.test import APITestCase, APIClient
from rest_framework_simplejwt.tokens import RefreshToken


class DrfTenantsClient(TenantClient, APIClient):
    pass


class DrfTenantsTestCase(APITestCase, TenantTestCase):
    def setUp(self):
        super().setUp()
        self.client = DrfTenantsClient(self.tenant)
        self._login()

    def _login(self):
        user = get_user_model().objects.create_user('Alvaro', 'alvaroscelza@gmail.com', 'password')
        refresh = RefreshToken.for_user(user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
