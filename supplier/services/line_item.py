from ..exceptions import LineItemNotFound
from ..model.line_items import LineItem
from ..serializers.line_items import LineItemSerializer


class LineItemService:
    def create_all_line_items_for_purchase_order(self, line_items, purchase_order):
        # Optimisation: We can insert via .bulk_create() as well
        line_items_objects = []
        for line_item in line_items:
            line_items_objects.append(self.create_line_item_for_purchase_order(line_item, purchase_order))
        serialized_line_items = LineItemSerializer(line_items_objects, many=True)
        return serialized_line_items.data

    def create_line_item_for_purchase_order(self, line_item, purchase_order):
        line_item = LineItem.objects.create(
            item_name=line_item["item_name"],
            quantity=line_item["quantity"],
            price_without_tax=line_item["price_without_tax"],
            tax_name=line_item["tax_name"],
            tax_total=line_item["tax_amount"],
            purchase_order=purchase_order
        )
        return line_item

    def get_items_for_purchase_order(self, purchase_order):
        line_items = LineItem.objects.filter(purchase_order=purchase_order)
        serialized_line_items = LineItemSerializer(line_items, many=True)
        return serialized_line_items.data

    def update_all_line_items_for_purchase_order(self, line_items, purchase_order):
        valid_line_items_for_purchase_order = []
        updated_line_items = []
        for line_item in line_items:
            line_item_id = line_item.get("id")
            if line_item_id:
                line_item_object = self.update_line_item_for_purchase_order_by_id(
                    line_item_id=line_item_id,
                    purchase_order=purchase_order,
                    line_item=line_item
                )
            else:
                line_item_object = self.create_line_item_for_purchase_order(
                    purchase_order=purchase_order,
                    line_item=line_item
                )
            valid_line_items_for_purchase_order.append(line_item_object.id)
            updated_line_items.append(line_item_object)
        self.delete_deprecated_line_items_for_purchase_order(
            valid_line_item_ids=valid_line_items_for_purchase_order,
            purchase_order=purchase_order
        )
        serialized_line_items = LineItemSerializer(updated_line_items, many=True)
        return serialized_line_items.data

    def update_line_item_for_purchase_order_by_id(self, line_item_id, purchase_order, line_item):
        try:
            line_item_object = LineItem.objects.get(purchase_order=purchase_order, id=line_item_id)
        except LineItem.DoesNotExist:
            raise LineItemNotFound(line_item_id)
        line_item_object.item_name = line_item["item_name"]
        line_item_object.quantity = line_item["quantity"]
        line_item_object.price_without_tax = line_item["price_without_tax"]
        line_item_object.tax_name = line_item["tax_name"]
        line_item_object.tax_total = line_item["tax_amount"]
        line_item_object.save()
        return line_item_object

    def delete_deprecated_line_items_for_purchase_order(self, valid_line_item_ids, purchase_order):
        deprecated_line_items = LineItem.objects.filter(purchase_order=purchase_order).exclude(id__in=valid_line_item_ids)
        if deprecated_line_items.exists():
            deprecated_line_items.delete()
