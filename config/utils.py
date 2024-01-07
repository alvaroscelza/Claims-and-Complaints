from django.core.mail import send_mail
from django.conf import settings
from django.utils.html import strip_tags
from django.template.loader import render_to_string


def send_html_email(
    subject,
    html_template,
    context,
    recipient,
    recipients=[],
    request=None,
    plaintext=None,
):
    # Set Recipient List
    recipient_list = recipients + [recipient] if recipient else []
    if not recipient_list:
        raise Exception("No Recipients found")
    # Base context values set incase of no request
    html_context = {"brand_name": settings.BRAND_NAME, "absolute_domain": "", **context}
    html = (
        render_to_string(html_template, request=request, context=html_context)
        if html_template
        else None
    )
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
