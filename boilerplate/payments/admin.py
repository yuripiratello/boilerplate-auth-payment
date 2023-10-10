from django.contrib import admin
from payments.models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "status", "created_at", "updated_at")
    search_fields = ("id", "user__email", "status")
    list_filter = ("status", "created_at", "updated_at")
