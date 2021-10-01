from django.contrib.auth.models import User
from django.db.models.query import QuerySet
from rest_framework import serializers

from .models import Order, OrderItem

from product.serializers import ProductSerializer

class MyOrderItemSerializer(serializers.ModelSerializer):    
    product = ProductSerializer()

    class Meta:
        model = OrderItem
        fields = (
            "price",
            "product",
            "quantity",
        )
class MyOrderSerializer(serializers.ModelSerializer):
    items = MyOrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ("id", "name", "email", "phone", "address", "note","created_at", "stripe_token", "items", "paid_amount", )

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields= ("price", "product", "quantity", )


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ("id", "name", "email", "phone", "address", "note", "stripe_token", "items", )

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        order = Order.objects.create(**validated_data)
        for item_data in items_data:
            OrderItem.objects.create(order=order, **item_data)

        return order

class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ("id", "username", "first_name", "last_name", "email", "password", "is_staff", "last_login", "date_joined", )
    

