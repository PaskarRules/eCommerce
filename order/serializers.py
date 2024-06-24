from rest_framework import serializers
from .models import Order


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ["id", "sku", "price", "delivery_date", "status", "user"]
        read_only_fields = ["user"]
