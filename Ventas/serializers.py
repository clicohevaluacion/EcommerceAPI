from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import *

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'name', 'price', 'stock')

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('id', 'date_time')

class OrderDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderDetail
        fields = ('order', 'cuantity', 'product')

class OrderwithDetailsSerializer(serializers.ModelSerializer):
    order = OrderDetailSerializer(many=True)

    class Meta:
        model = Order
        fields = ('id', 'date_time', 'order')

