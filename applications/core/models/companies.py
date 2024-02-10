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
        # noinspection PyUnresolvedReferences
        return sum(j.vote for j in self.judgement_set.all()) or 0
