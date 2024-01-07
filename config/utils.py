from django.core.mail import send_mail
from django.conf import settings
from django.utils.html import strip_tags


def send_html_email(subject, html, plaintext, recipient, recipients=[]):
    # Set Recipient List
    recipient_list = recipients + [recipient] if recipient else []
    if not recipient_list:
        raise Exception("No Recipients found")
    # Send Email
    send_mail(
        subject,
        plaintext or strip_tags(html),
        f"{settings.EMAIL_FROM_NAME}<{settings.EMAIL_HOST_USER}>",
        recipient_list,
        fail_silently=settings.IS_PRODUCTION,
        html_message=html,
    )
    # Return true if successful
    return True
