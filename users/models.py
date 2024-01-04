from django.db import models
from django.contrib.auth.models import AbstractUser
from applications.utils import UniqueNameMixin


# User model inherits from Django's Existing model to retain built in functionality
class User(AbstractUser):
    # User Profile Attributes
    profile_picture = models.ImageField(upload_to="user/", blank=True, null=True)

    # User Login/Signup Attributes
    email_validated = models.DateTimeField(blank=True, null=True, db_index=True)
    email_invalid = models.DateTimeField(
        blank=True,
        null=True,
        db_index=True,
        help_text="Date user email was marked as invalid",
    )
    # User Tracking
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def score(self) -> int:
        # noinspection PyUnresolvedReferences
        score_modifiers = self.user_score_modifier_instance_set
        return (
            score_modifiers.aggregate(models.Sum("modifier_type__score"))[
                "modifier_type__score__sum"
            ]
            or 0
        )

    def send_verification_email(self):
        pass

    def send_forgot_password_email(self):
        pass

    # todo


class UserScoreModifierType(UniqueNameMixin):
    score = models.IntegerField()


class UserScoreModifierInstance(models.Model):
    user = models.ForeignKey("User", models.CASCADE)
    modifier_type = models.ForeignKey(UserScoreModifierType, models.CASCADE)
    date_time = models.DateTimeField(auto_now_add=True)
