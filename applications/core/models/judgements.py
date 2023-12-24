from django.db import models

from applications.core.models.companies import Company
from applications.core.models.users import ClientUser


class Judgement(models.Model):
    opinion = models.TextField()
    vote = models.BooleanField()
    author = models.ForeignKey(ClientUser, models.CASCADE)
    company = models.ForeignKey(Company, models.CASCADE)
