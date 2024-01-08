from order.exceptions import PurchaseOrderNotFound
from order.models.purchase_order import PurchaseOrder


class PurchaseOrderService:
    def create_purchase_order(self, supplier_object, total_amount, total_quantity, total_tax):
        return PurchaseOrder.objects.create(
            supplier=supplier_object,
            total_amount=total_amount,
            total_quantity=total_quantity,
            total_tax=total_tax
        )

    def get_purchase_order_object_by_id(self, purchase_order_id):
        try:
            purchase_order = PurchaseOrder.objects.get(id=purchase_order_id)
        except PurchaseOrder.DoesNotExist:
            raise PurchaseOrderNotFound(purchase_order_id)
        return purchase_order

    def get_purchase_orders_by_supplier_name_and_line_item_name(self, supplier_name, item_name):
        return PurchaseOrder.objects.filter(
                supplier__name__icontains=supplier_name, lineitem__item_name__icontains=item_name
            )

    def get_purchase_orders_by_supplier_name(self, supplier_name):
        return PurchaseOrder.objects.filter(
                supplier__name__icontains=supplier_name
            )

    def get_purchase_orders_by_item_name(self, item_name):
        return PurchaseOrder.objects.filter(
                lineitem__item_name__icontains=item_name
            )

    def get_all_purchase_orders(self):
        return PurchaseOrder.objects.all()
