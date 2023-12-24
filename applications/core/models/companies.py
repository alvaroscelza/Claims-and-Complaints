from django.db import models

from applications.utils import UniqueNameMixin


class Business(UniqueNameMixin):
    pass


class Company(UniqueNameMixin):
    business = models.ForeignKey(Business, models.PROTECT)
    score = models.IntegerField(default=0)
    logo = models.ImageField(upload_to='company/', blank=True, null=True)
    description = models.TextField(blank=True, null=True)
