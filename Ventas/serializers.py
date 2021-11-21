from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import *

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'name', 'price', 'stock')

class OrderSerializer(serializers.ModelSerializer):
    total_price = serializers.ReadOnlyField(source='get_total')
    total_price_usd = serializers.ReadOnlyField(source='get_total_usd')

    class Meta:
        model = Order
        fields = ('id', 'date_time', 'total_price','total_price_usd')


class OrderDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderDetail
        fields = ('order', 'cuantity', 'product')

class OrderwithDetailsSerializer(serializers.ModelSerializer):
    order = OrderDetailSerializer(many=True)
    total_price = serializers.ReadOnlyField(source='get_total')
    total_price_usd = serializers.ReadOnlyField(source='get_total_usd')

    class Meta:
        model = Order
        fields = ('id', 'date_time', 'total_price','total_price_usd', 'order')

