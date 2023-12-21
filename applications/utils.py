from django.core.exceptions import ValidationError as DjangoValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import ValidationError as DRFValidationError
from rest_framework.views import exception_handler as drf_exception_handler


class UniqueNameMixin(models.Model):
    class Meta:
        abstract = True

    name = models.CharField(_('name'), max_length=100, unique=True)

    def __str__(self):
        return self.name


def exception_handler(exc, context):
    """
    Handle Django ValidationError as an accepted exception by DRF.
    For the parameters, see ``exception_handler``
    """

    if isinstance(exc, DjangoValidationError):
        exc = DRFValidationError(detail=exc.message_dict)
    return drf_exception_handler(exc, context)
