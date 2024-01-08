from django.db import transaction

from supplier.services.line_item import LineItemService
from supplier.services.supplier import SupplierService
from ..exceptions import PurchaseOrderNotFound
from ..models.purchase_order import PurchaseOrder
from ..serializers.purchase_order import PurchaseOrderSerialzier


class PurchaseOrderService:
    """
        Service class to handle operations related to PurchaseOrder instances.

        Methods:
        - create(data)
        - get_by_id(purchase_order_id)
        - update(purchase_order_id, data)
        - delete_by_id(purchase_order_id)
        - get_by_query_params(query_params)
        - get_supplier_data_from_request(data)
        - get_line_item_data_from_request(data):
        - get_total_quantity_of_order(line_items_data)
        - get_total_amount_of_order(line_items_data)
        - get_total_tax_of_order(line_items_data)
        - update_purchase_order_by_id(purchase_order_id, updated_quantity, updated_total_amount, updated_total_tax, updated_supplier)
    """
    line_item_service = LineItemService()
    supplier_service = SupplierService()

    @transaction.atomic
    def create(self, data):
        """
        Creates a PurchaseOrder with associated Supplier and LineItems.

        Args:
        - data (dict): Data containing Supplier and LineItems information.

        Returns:
        - dict: Serialized data of the created PurchaseOrder and its LineItems.
        """
        supplier_data = self.get_supplier_data_from_request(data)
        line_items_data = self.get_line_item_data_from_request(data)
        supplier_object = self.supplier_service.update_or_create(**supplier_data)
        total_quantity = self.get_total_quantity_of_order(line_items_data)
        total_amount = self.get_total_amount_of_order(line_items_data)
        total_tax = self.get_total_tax_of_order(line_items_data)
        purchase_order = PurchaseOrder.objects.create(
            supplier=supplier_object,
            total_amount=total_amount,
            total_quantity=total_quantity,
            total_tax=total_tax
        )
        serialized_line_items_after_saving = self.line_item_service.create_all_line_items_for_purchase_order(
            line_items=line_items_data, purchase_order=purchase_order
        )
        return {
            **PurchaseOrderSerialzier(purchase_order).data,
            "line_items": serialized_line_items_after_saving,
        }

    def get_by_id(self, purchase_order_id):
        """
        Retrieves a PurchaseOrder by its ID.

        Args:
        - purchase_order_id (int): ID of the PurchaseOrder.

        Returns:
        - dict: Serialized data of the PurchaseOrder and its LineItems.
        """
        try:
            purchase_order = PurchaseOrder.objects.get(id=purchase_order_id)
        except PurchaseOrder.DoesNotExist:
            raise PurchaseOrderNotFound(purchase_order_id)
        line_items = self.line_item_service.get_items_for_purchase_order(purchase_order)
        complete_purchase_order_data = PurchaseOrderSerialzier(purchase_order).data
        complete_purchase_order_data["line_items"] = line_items
        return complete_purchase_order_data

    @transaction.atomic
    def update(self, purchase_order_id, data):
        """
        Updates a PurchaseOrder with updated details.

        Args:
        - purchase_order_id (int): ID of the PurchaseOrder to update.
        - data (dict): Updated data for the PurchaseOrder.

        Returns:
        - dict: Serialized data of the updated PurchaseOrder and its LineItems.
        """
        supplier_data = self.get_supplier_data_from_request(data)
        line_items_data = self.get_line_item_data_from_request(data)
        supplier_object = self.supplier_service.update_or_create(**supplier_data)
        total_quantity = self.get_total_quantity_of_order(line_items_data)
        total_amount = self.get_total_amount_of_order(line_items_data)
        total_tax = self.get_total_tax_of_order(line_items_data)
        purchase_order = self.update_purchase_order_by_id(
            purchase_order_id=purchase_order_id,
            updated_quantity=total_quantity,
            updated_total_amount=total_amount,
            updated_total_tax=total_tax,
            updated_supplier=supplier_object
        )
        serialized_line_items_after_saving = self.line_item_service.update_all_line_items_for_purchase_order(
            line_items=line_items_data, purchase_order=purchase_order
        )
        return {
            **PurchaseOrderSerialzier(purchase_order).data,
            "line_items": serialized_line_items_after_saving,
        }

    def delete_by_id(self, purchase_order_id):
        """
        Deletes a PurchaseOrder by its ID.
        """
        try:
            purchase_object = PurchaseOrder.objects.get(id=purchase_order_id)
        except PurchaseOrder.DoesNotExist:
            raise PurchaseOrderNotFound(purchase_order_id)
        purchase_object.delete()

    def get_by_query_params(self, query_params):
        """
        Retrieves PurchaseOrders based on query parameters.
        """
        supplier_name = query_params.get("supplier_name")
        item_name = query_params.get("item_name")
        response_data = []
        if supplier_name and item_name:
            purchase_orders = PurchaseOrder.objects.filter(
                supplier__name__icontains=supplier_name, lineitem__item_name__icontains=item_name
            )
        elif supplier_name:
            purchase_orders = PurchaseOrder.objects.filter(
                supplier__name__icontains=supplier_name
            )
        elif item_name:
            purchase_orders = PurchaseOrder.objects.filter(
                lineitem__item_name__icontains=item_name
            )
        else:
            purchase_orders = PurchaseOrder.objects.all()
        for purchase_order in purchase_orders:
            line_items = self.line_item_service.get_items_for_purchase_order(purchase_order)
            response_data.append(
                {
                    **PurchaseOrderSerialzier(purchase_order).data,
                    "line_items": line_items,
                }
            )
        return response_data

    def get_supplier_data_from_request(self, data):
        """
        Extracts Supplier data from a request.
        """
        supplier_data = data.get("supplier")
        supplier_data["supplier_id"] = supplier_data.get("id", None)
        supplier_data.pop("id", None)
        return supplier_data

    def get_line_item_data_from_request(self, data):
        """
        Extracts LineItems data from a request.
        """
        line_items = data.get("line_items")
        for line_item in line_items:
            line_item["price_without_tax"] = float(line_item["price_without_tax"])
            line_item["tax_total"] = float(line_item["tax_amount"])
        return line_items

    def get_total_quantity_of_order(self, line_items_data):
        """
        Calculates the total quantity of LineItems.
        """
        total_quantity_of_order = 0
        for line_item in line_items_data:
            total_quantity_of_order += line_item['quantity']
        return total_quantity_of_order

    def get_total_amount_of_order(self, line_items_data):
        """
        Calculates the total amount of the Order.
        """
        total_amount = 0
        for line_item in line_items_data:
            total_amount += (line_item['price_without_tax']+line_item['tax_total'])
        return total_amount

    def get_total_tax_of_order(self, line_items_data):
        """
        Calculates the total tax of the Order.
        """
        total_tax = 0
        for line_item in line_items_data:
            total_tax += line_item['tax_total']
        return total_tax

    def update_purchase_order_by_id(self, purchase_order_id, updated_quantity, updated_total_amount,
                                    updated_total_tax, updated_supplier):
        """
        Updates a PurchaseOrder by ID.
        """
        try:
            purchase_object = PurchaseOrder.objects.get(id=purchase_order_id)
        except PurchaseOrder.DoesNotExist:
            raise PurchaseOrderNotFound(purchase_order_id)
        purchase_object.total_tax = updated_total_tax
        purchase_object.supplier = updated_supplier
        purchase_object.total_amount = updated_total_amount
        purchase_object.total_quantity = updated_quantity
        purchase_object.save()
        return purchase_object
