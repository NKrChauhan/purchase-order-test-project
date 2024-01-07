from rest_framework import serializers

from supplier.serializers.supplier import SupplierSerializer


class PurchaseOrderSerialzier(serializers.Serializer):
    id = serializers.IntegerField()
    supplier = SupplierSerializer()
    order_time = serializers.DateTimeField()
    order_number = serializers.IntegerField()
    total_quantity = serializers.IntegerField()
    total_amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    total_tax = serializers.DecimalField(max_digits=10, decimal_places=2)
