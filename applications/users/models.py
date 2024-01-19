from django.contrib.auth.models import AbstractUser
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.db import models
from django.urls import reverse

from applications.utils import UniqueNameMixin
from config.utils import send_html_email


class User(AbstractUser):
    profile_picture = models.ImageField(upload_to='user/', blank=True, null=True)
    email_validated = models.DateTimeField(blank=True, null=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def score(self) -> int:
        # noinspection PyUnresolvedReferences
        score_modifiers = self.user_score_modifier_instance_set
        return score_modifiers.aggregate(models.Sum('modifier_type__score'))['modifier_type__score__sum'] or 0

    def send_verification_email(self, request=None):
        token_generator = PasswordResetTokenGenerator()
        token = token_generator.make_token(self)
        url = reverse('users:verify_email', kwargs={'user_id': self.pk, 'token': token})
        send_html_email(
            html_template='users/emails/register_verification.html',
            context={'url': url, 'user': self},
            subject='Verify your Account',
            recipient=self.email,
            request=request,
        )

    def send_forgot_password_email(self, request=None):
        token_generator = PasswordResetTokenGenerator()
        token = token_generator.make_token(self)
        url = reverse('users:forgot_password', kwargs={'token': token, 'user_id': self.pk})
        send_html_email(
            html_template='users/emails/forgot_password.html',
            context={'url': url, 'user': self},
            subject='Verify your Account',
            recipient=self.email,
            request=request,
        )


class UserScoreModifierType(UniqueNameMixin):
    score = models.IntegerField()


class UserScoreModifierInstance(models.Model):
    user = models.ForeignKey(User, models.CASCADE)
    modifier_type = models.ForeignKey(UserScoreModifierType, models.CASCADE)
    date_time = models.DateTimeField(auto_now_add=True)
