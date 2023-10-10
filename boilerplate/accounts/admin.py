from django.contrib import admin
from accounts.models import Team


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ("owner", "created_at", "updated_at")
    search_fields = ("owner__username", "owner__email")
    list_filter = ("created_at", "updated_at")
    readonly_fields = ("created_at", "updated_at")
    filter_horizontal = ("members",)
