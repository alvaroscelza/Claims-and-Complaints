from django.contrib.auth.models import User
from django.db import models

from applications.utils import UniqueNameMixin


class UserScoreModifierType(UniqueNameMixin):
    score = models.IntegerField()


class ClientUser(User):
    profile_picture = models.ImageField(upload_to='user/', blank=True, null=True)

    @property
    def score(self) -> int:
        # noinspection PyUnresolvedReferences
        score_modifiers = self.user_score_modifier_instance_set
        return score_modifiers.aggregate(models.Sum('modifier_type__score'))['modifier_type__score__sum'] or 0


class UserScoreModifierInstance(models.Model):
    user = models.ForeignKey(ClientUser, models.CASCADE)
    modifier_type = models.ForeignKey(UserScoreModifierType, models.CASCADE)
    date_time = models.DateTimeField(auto_now_add=True)
