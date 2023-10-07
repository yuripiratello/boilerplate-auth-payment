from django.db import models
from django.utils.translation import gettext as _
from boilerplate.utils import BaseModel


class ProductTag(models.Model):
    name = models.CharField(
        _("Name"),
        max_length=100,
        help_text=_("Designates the name of the tag."),
    )

    def __str__(self) -> str:
        return self.name


class Product(BaseModel):
    name = models.CharField(
        _("Name"),
        max_length=100,
    )
    description = models.TextField(verbose_name=_("Description"))
    tags = models.ManyToManyField(
        ProductTag,
        blank=True,
        related_name="products",
        verbose_name=_("Tags"),
    )
    thumbnail = models.ImageField(
        upload_to="products",
        blank=True,
        null=True,
        verbose_name=_("Thumbnail"),
    )
    url = models.URLField(verbose_name=_("URL"))
    quantity = models.IntegerField(
        default=1,
        verbose_name=_("Quantity"),
    )

    def __str__(self):
        return self.name


class Price(BaseModel):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="prices",
        verbose_name="Product",
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_("Price"),
    )
