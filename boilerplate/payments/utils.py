import stripe
from django.conf import settings
from payments.models import Payment

stripe.api_key = settings.STRIPE_SECRET_KEY


def create_stripe_link(payment: Payment, price_id: str) -> stripe.checkout.Session:
    checkout_session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[
            {
                "price": price_id,
                "quantity": 1,
            },
        ],
        metadata={
            "payment_id": payment.id,
        },
        mode=payment.payment_type,
        customer_email=payment.user.email,
        success_url="http://localhost:8000/success",
        cancel_url="http://localhost:8000/cancel",
    )
    payment.checkout_session_id = checkout_session.id
    payment.save()
    return checkout_session


def new_payment(payment_intention, user) -> Payment:
    payment_intention_data = payment_intention.validated_data
    price = stripe.Price.retrieve(
        payment_intention_data.get("price"), expand=["product"]
    )
    payment_type = price.product.metadata.get("payment_type")
    payment = Payment.objects.create(
        user=user,
        status=Payment.PaymentStatus.PENDING,
        payment_type=payment_type,
    )
    return payment
