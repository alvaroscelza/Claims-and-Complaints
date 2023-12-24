from django.db import models

from applications.core.models.companies import Company
from applications.core.models.users import ClientUser


class Votes(models.IntegerChoices):
    VERY_BAD = -2
    BAD = -1
    NEUTRAL = 0
    GOOD = 1
    VERY_GOOD = 2


class Judgement(models.Model):
    opinion = models.TextField()
    vote = models.IntegerField(choices=Votes.choices)
    author = models.ForeignKey(ClientUser, models.CASCADE)
    company = models.ForeignKey(Company, models.CASCADE)
