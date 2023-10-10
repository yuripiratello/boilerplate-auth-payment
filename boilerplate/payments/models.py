from django.db import models
from django.conf import settings
from django.utils.translation import gettext as _
from boilerplate.utils import BaseModel


class Payment(BaseModel):
    class PaymentStatus(models.TextChoices):
        PENDING = "pending", _("Pending")
        COMPLETED = "completed", _("Completed")
        FAILED = "failed", _("Failed")
        CANCELED = "canceled", _("Canceled")

    class PaymentType(models.TextChoices):
        SUBSCRIPTION = "subscription", _("Subscription")
        ONE_TIME = "payment", _("One Time Payment")

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="payments",
        verbose_name=_("User"),
    )
    status = models.CharField(
        max_length=100,
        choices=PaymentStatus.choices,
        verbose_name=_("Status"),
        default=PaymentStatus.PENDING,
    )
    payment_type = models.CharField(
        max_length=100,
        choices=PaymentType.choices,
        verbose_name=_("Payment Type"),
    )
    checkout_session_id = models.CharField(
        max_length=255,
        verbose_name=_("Checkout Sesion ID"),
        blank=True,
        null=True,
    )
