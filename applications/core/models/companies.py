from django.db import models
from django.utils.translation import gettext as _

from applications.utils import UniqueNameMixin


class Business(UniqueNameMixin):
    class Meta(UniqueNameMixin.Meta):
        verbose_name = _('business')
        verbose_name_plural = _('businesses')


class Company(UniqueNameMixin):
    class Meta(UniqueNameMixin.Meta):
        verbose_name = _('company')
        verbose_name_plural = _('companies')

    business = models.ForeignKey(Business, models.PROTECT)
    logo = models.ImageField(upload_to='company/', blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    @property
    def score(self) -> int:
        # noinspection PyUnresolvedReferences
        return sum(j.vote for j in self.judgement_set.all()) or 0
