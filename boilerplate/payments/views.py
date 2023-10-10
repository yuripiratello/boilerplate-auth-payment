import stripe
from pprint import pprint
from django.db import transaction
from django.conf import settings
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.shortcuts import get_object_or_404
from payments.utils import new_payment, create_stripe_link
from payments.serializers import PaymentIntentionSerializer
from payments.models import Payment

stripe.api_key = settings.STRIPE_SECRET_KEY


class CheckoutLinkView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        payment_intention = PaymentIntentionSerializer(data=request.data)
        if not payment_intention.is_valid():
            return Response(
                data=payment_intention.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )
        with transaction.atomic():
            payment = new_payment(
                payment_intention=payment_intention,
                user=request.user,
            )
            checkout_session = create_stripe_link(
                payment,
                payment_intention.validated_data.get("price"),
            )
            return Response(
                data={"checkout_url": checkout_session.url},
                status=status.HTTP_200_OK,
            )


class ProductsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        products_list = stripe.Price.list(
            product="prod_Omxr1g2SEhwtwo",
            expand=["data.product"],
        )
        return Response(
            {
                "prices": products_list["data"],
            },
            status=status.HTTP_200_OK,
        )


@method_decorator(csrf_exempt, name="dispatch")
class StripeWebhookView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, format=None):
        payload = request.body
        endpoint_secret = settings.STRIPE_WEBHOOK_SECRET
        sig_header = request.META["HTTP_STRIPE_SIGNATURE"]
        event = None
        try:
            event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
        except ValueError:
            # Invalid payload
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except stripe.error.SignatureVerificationError:
            # Invalid signature
            return Response(status=status.HTTP_400_BAD_REQUEST)
        if event["type"] == "checkout.session.completed":
            pprint(event, indent=2)
            session = event["data"]["object"]
            payment_id = session["metadata"]["payment_id"]
            payment = get_object_or_404(
                Payment,
                id=payment_id,
            )
            payment.status = "completed"
            payment.save()

        return Response(status=status.HTTP_200_OK)
