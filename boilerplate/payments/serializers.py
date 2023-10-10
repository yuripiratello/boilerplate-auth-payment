from rest_framework import serializers


class PaymentIntentionSerializer(serializers.Serializer):
    price = serializers.CharField(required=True)
