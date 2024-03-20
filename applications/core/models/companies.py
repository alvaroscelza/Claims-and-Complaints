from django.db import models
from django.utils.translation import gettext as _

from applications.utils import UniqueNameMixin


class Industry(UniqueNameMixin):
    class Meta(UniqueNameMixin.Meta):
        verbose_name = _('industry')
        verbose_name_plural = _('industries')


class Company(UniqueNameMixin):
    class Meta(UniqueNameMixin.Meta):
        verbose_name = _('company')
        verbose_name_plural = _('companies')

    industry = models.ForeignKey(Industry, models.PROTECT)
    logo = models.ImageField(upload_to='company/', blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    @property
    def score(self) -> int:
        score = 0
        # noinspection PyUnresolvedReferences
        for branch in self.companybranch_set.all():
            for judgement in branch.judgement_set.all():
                score += judgement.vote
        return score


class CompanyBranch(UniqueNameMixin):
    class Meta(UniqueNameMixin.Meta):
        verbose_name = _('company branch')
        verbose_name_plural = _('companies branches')

    address = models.TextField(blank=True, null=True)
    company = models.ForeignKey(Company, models.CASCADE)

    @property
    def score(self) -> int:
        # noinspection PyUnresolvedReferences
        return sum(j.vote for j in self.judgement_set.all()) or 0
