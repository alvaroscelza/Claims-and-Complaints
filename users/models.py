import os
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from applications.utils import UniqueNameMixin
from config.utils import send_html_email
from .token import account_activation_token, account_password_reset_token


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

    @property
    def profile_picture_filename(self):
        if not self.profile_picture:
            return None
        return os.path.basename(self.profile_picture.name)

    def get_activate_url(self):
        token = account_activation_token.make_token(self)
        return reverse("users:verify_email", kwargs={"user_id": self.id, token: token})

    def get_password_reset_url(self):
        token = account_password_reset_token.make_token(self)
        return reverse(
            "users:forgot_password", kwargs={"token": token, "user_id": self.id}
        )

    def send_verification_email(self, request=None):
        url = self.get_activate_url()
        send_html_email(
            html_template="users/emails/register_verification.html",
            context={"url": url, "user": self},
            subject="Verify your Account",
            recipient=self.email,
            request=request,
        )

    def send_forgot_password_email(self, request=None):
        url = self.get_password_reset_url()
        send_html_email(
            html_template="users/emails/forgot_password.html",
            context={"url": url, "user": self},
            subject="Verify your Account",
            recipient=self.email,
            request=request,
        )


class UserScoreModifierType(UniqueNameMixin):
    score = models.IntegerField()


class UserScoreModifierInstance(models.Model):
    user = models.ForeignKey("User", models.CASCADE)
    modifier_type = models.ForeignKey(UserScoreModifierType, models.CASCADE)
    date_time = models.DateTimeField(auto_now_add=True)
