from django.conf import settings
from django.db import models
from django.utils.translation import gettext as _
from boilerplate.utils import BaseModel


class Profile(BaseModel):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile",
        verbose_name=_("User"),
    )
    user_type = models.CharField(
        max_length=100,
        verbose_name=_("User Type"),
        choices=(
            ("admin", _("Admin")),
            ("customer", _("Customer")),
            ("member", _("Member")),
        ),
    )
    avatar = models.ImageField(
        upload_to="profiles",
        blank=True,
        null=True,
        verbose_name=_("Avatar"),
    )
    company = models.CharField(
        max_length=100,
        verbose_name=_("Company"),
        blank=True,
        null=True,
    )


class Team(BaseModel):
    name = models.CharField(
        max_length=100,
        verbose_name=_("Name"),
    )
    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="teams",
        verbose_name=_("Members"),
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="owned_teams",
        verbose_name=_("Owner"),
    )

    def __str__(self) -> str:
        return self.name
