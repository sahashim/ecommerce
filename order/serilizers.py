from rest_framework import serializers

from .models import Order, OrderItem, Coupon


class OrderSerializer(serializers.ModelSerializer):
    """
    The order model serializer.
    """

    class Meta:
        model = Order
        fields = '__all__'


class OrderItemSerializer(serializers.ModelSerializer):
    """
    The order item model serializer.
    """

    class Meta:
        model = OrderItem
        fields = '__all__'


class CouponSerializer(serializers.ModelSerializer):
    """
    The Coupon model serializer.
    """
    class Meta:
        model = Coupon
        fields = '__all__'
