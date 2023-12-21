from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.exceptions import APIException


class PaymentRequired(APIException):
    status_code = status.HTTP_402_PAYMENT_REQUIRED
    default_detail = _('This action requires payment.')
    default_code = 'payment_required'
