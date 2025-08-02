from rest_framework import serializers
from products.serializers import ProductSerializer
from .models import Order, OrderItem

class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'price', 'quantity']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'status', 'delivery_address', 'total_price', 'arrival_date', 'created_at', 'paid', 'items']
        read_only_fields = ['id', 'created_at']