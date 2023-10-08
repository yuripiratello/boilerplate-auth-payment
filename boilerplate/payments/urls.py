from django.urls import path

from payments.views import StripeWebhookView

app_name = "payments"

urlpatterns = [
    path("webhooks/stripe/", StripeWebhookView.as_view(), name="stripe-webhook"),
]
