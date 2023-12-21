import os

from django.contrib.auth.models import User
from django.db import models
from django_tenants.utils import schema_context


class OrganizationsManager(models.QuerySet):
    def create(self, **kwargs):
        organization = super().create(**kwargs)
        domain = os.getenv('DOMAIN', 'localhost')
        organization.domains.create(domain=f'{organization.schema_name}.{domain}', is_primary=True)
        self.create_tenant_superuser(organization.schema_name)
        return organization

    @staticmethod
    def create_tenant_superuser(schema_name):
        with schema_context(schema_name):
            email = 'admin@admin.com'
            password = os.getenv('DJANGO_SUPERUSER_PASSWORD', 'admin.123')
            User.objects.create_superuser(username='admin', email=email, password=password)
