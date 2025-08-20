from rest_framework import serializers

from orders.models import Item, Order


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = "__all__"


class OrderSerializer(serializers.ModelSerializer):
    item_set = ItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = "__all__"
