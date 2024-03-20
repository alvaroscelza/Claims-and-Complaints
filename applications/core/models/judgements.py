from django.conf import settings
from django.db import models

from applications.core.models.companies import CompanyBranch


class Votes(models.IntegerChoices):
    VERY_BAD = -2
    BAD = -1
    GOOD = 1
    VERY_GOOD = 2


class Judgement(models.Model):
    opinion = models.TextField()
    vote = models.IntegerField(choices=Votes.choices)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, models.CASCADE)
    company_branch = models.ForeignKey(CompanyBranch, models.CASCADE)
