from django.db import models
from django_tenants.models import TenantMixin, DomainMixin

from applications.tenants.managers.organizations_manager import OrganizationsManager


class Organization(TenantMixin):
    objects = OrganizationsManager.as_manager()

    name = models.CharField(max_length=100)


class Domain(DomainMixin):
    pass
