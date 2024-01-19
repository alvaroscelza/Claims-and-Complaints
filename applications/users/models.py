from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import send_mail
from django.db import models
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.html import strip_tags

from applications.utils import UniqueNameMixin


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
        self._send_html_email(
            html_template='users/emails/register_verification.html',
            context={'url': url, 'user': self},
            subject='Verify your Account',
            recipient=self.email,
            request=request,
        )

    @staticmethod
    def _send_html_email(subject, html_template, context, recipient, recipients=[], request=None, plaintext=None):
        # Set Recipient List
        recipient_list = recipients + [recipient] if recipient else []
        if not recipient_list:
            raise Exception('No Recipients found')
        # Base context values set incase of no request
        html_context = {
            'brand_name': settings.BRAND_NAME,
            'absolute_domain': request.build_absolute_uri('/')[:-1]
            if request
            else settings.SITE_URL,
            **context,
        }
        html = (
            render_to_string(html_template, request=request, context=html_context)
            if html_template
            else None
        )
        # Send Email
        send_mail(
            subject,
            plaintext or strip_tags(html),
            f'{settings.EMAIL_FROM_NAME}<{settings.EMAIL_HOST_USER}>',
            recipient_list,
            fail_silently=settings.IS_PRODUCTION,
            html_message=html,
        )
        # Return true if successful
        return True

    def send_forgot_password_email(self, request=None):
        token_generator = PasswordResetTokenGenerator()
        token = token_generator.make_token(self)
        url = reverse('users:forgot_password', kwargs={'token': token, 'user_id': self.pk})
        self._send_html_email(
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
