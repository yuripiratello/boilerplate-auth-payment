from django.conf import settings
from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _
from boilerplate.utils import BaseModel


class Profile(BaseModel):
    class UserType(models.TextChoices):
        ADMIN = "admin", _("Admin")
        CUSTOMER = "customer", _("Customer")
        MEMBER = "member", _("Member")

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile",
        verbose_name=_("User"),
    )
    user_type = models.CharField(
        max_length=100,
        verbose_name=_("User Type"),
        choices=UserType.choices,
        default=UserType.CUSTOMER,
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
    active = models.BooleanField(
        default=True,
        verbose_name=_("Active"),
    )

    def has_plan(self):
        user = None
        if self.user_type == self.UserType.ADMIN:
            user = self.user
        else:
            user = self.user.team_set.first().owner
        return user.payments.filter(active=True).exists()


class Team(BaseModel):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="owned_teams",
        verbose_name=_("Owner"),
    )
    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="teams",
        verbose_name=_("Members"),
    )

    def __str__(self) -> str:
        return self.owner.username

    def create_and_add_member(self, member_data):
        member = get_user_model().objects.create(
            username=member_data.get("username"),
            email=member_data.get("email"),
            first_name=member_data.get("first_name"),
            last_name=member_data.get("last_name"),
        )
        member.save()
        self.members.add(member)
        # TODO: send email to the user to reset/create password
        self.save()
        return member
