from rest_framework import serializers

from myshop.models import Item, Order, Refund


class ItemSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'


class OrderSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'


class RefundSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Refund
        fields = '__all__'
