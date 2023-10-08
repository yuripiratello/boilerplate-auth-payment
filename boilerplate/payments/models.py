from django.db import models
from django.conf import settings
from django.utils.translation import gettext as _
from boilerplate.utils import BaseModel


class Purchase(BaseModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="purchases",
        verbose_name=_("User"),
    )
    total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_("Total"),
    )
    discount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_("Discount"),
    )
    status = models.CharField(
        max_length=100,
        choices=(
            ("pending", _("Pending")),
            ("completed", _("Completed")),
            ("failed", _("Failed")),
            ("canceled", _("Canceled")),
        ),
        verbose_name=_("Status"),
    )
    # TODO: Any other purchase type? Change to model?
    purchase_type = models.CharField(
        max_length=100,
        choices=(
            ("subscription", _("Subscription")),
            ("one time", _("One Time")),
        ),
        verbose_name=_("Purchase Type"),
    )
    coupon = models.ForeignKey(
        "Coupon",
        on_delete=models.CASCADE,
        related_name="purchases",
        verbose_name=_("Coupon"),
    )


class Coupon(BaseModel):
    code = models.CharField(
        max_length=100,
        verbose_name=_("Code"),
    )
    discount_value = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_("Discount Value"),
        blank=True,
        null=True,
    )
    discount_percentage = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_("Discount Percentage"),
        blank=True,
        null=True,
    )
    products = models.ManyToManyField(
        "products.Product",
        blank=True,
        related_name="coupons",
        verbose_name=_("Products"),
    )
    additional = models.ManyToManyField(
        "PurchaseAdditional",
        blank=True,
        related_name="coupons",
        verbose_name=_("Additional"),
    )
    quantity = models.IntegerField(
        verbose_name=_("Quantity"),
    )
    expiration = models.DateTimeField(
        verbose_name=_("Expiration"),
    )


class PurchaseProduct(BaseModel):
    purchase = models.ForeignKey(
        Purchase,
        on_delete=models.CASCADE,
        related_name="products",
        verbose_name=_("Purchase"),
    )
    product = models.ForeignKey(
        "products.Product",
        on_delete=models.CASCADE,
        related_name="purchases",
        verbose_name=_("Product"),
    )
    quantity = models.IntegerField(
        verbose_name=_("Quantity"),
    )
    currency = models.CharField(
        max_length=3,
        verbose_name=_("Currency"),
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_("Price"),
    )
    discount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_("Discount"),
    )


class PurchaseAdditional(BaseModel):
    purchase = models.ForeignKey(
        Purchase,
        on_delete=models.CASCADE,
        related_name="additionals",
        verbose_name=_("Purchase"),
    )
    product = models.ForeignKey(
        "products.Product",
        on_delete=models.CASCADE,
        related_name="additionals",
        verbose_name=_("Product"),
    )
    quantity = models.IntegerField(
        verbose_name=_("Quantity"),
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_("Price"),
    )
    discount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_("Discount"),
    )
