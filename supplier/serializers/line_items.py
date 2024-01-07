from rest_framework import serializers


class LineItemSerializer(serializers.Serializer):
    item_name = serializers.CharField()
    quantity = serializers.IntegerField()
    price_without_tax = serializers.DecimalField(max_digits=10, decimal_places=2)
    tax_name = serializers.CharField()
    tax_total = serializers.DecimalField(max_digits=10, decimal_places=2)
    line_total = serializers.DecimalField(max_digits=10, decimal_places=2)
