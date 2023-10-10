from django.urls import path

from payments.views import StripeWebhookView, CheckoutLinkView, ProductsView

app_name = "payments"

urlpatterns = [
    path("webhooks/stripe/", StripeWebhookView.as_view(), name="stripe-webhook"),
    path("prices/", ProductsView.as_view(), name="prices"),
    path("checkout/", CheckoutLinkView.as_view(), name="checkout-link"),
]
