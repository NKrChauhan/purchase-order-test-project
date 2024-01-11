from django.urls import reverse
from rest_framework.test import APITestCase

from order.tests.factory.purchase_order import PurchaseOrderFactory
from supplier.model.line_items import LineItem
from supplier.tests.factory.line_item import LineItemFactory
from supplier.tests.factory.supplier import SupplierFactory


class PurchaseOrderViewTest(APITestCase):
    def setUp(self) -> None:
        self.supplier = SupplierFactory.create()
        self.purchase_order = PurchaseOrderFactory.create(
            supplier=self.supplier,
            total_quantity=4,
            total_tax=1.00,
            total_amount=5.00
        )
        self.line_items = LineItemFactory.build_batch(
            size=2, purchase_order=self.purchase_order, quantity=2, price_without_tax=2.0, tax_total=0.5, item_name="test_product"
        )
        for line_item in self.line_items: line_item.save()

    def test_purchase_order_creation_request(self):
        request_data = {
            "supplier": {
                "id": None,
                "name": "my supplier",
                "email": "email@email.com"
            },
            "line_items": [
                {
                  "item_name": "test prod",
                  "quantity": 1,
                  "price_without_tax": "10.00",
                  "tax_name": "GST 5%",
                  "tax_amount": "0.50"
                }
            ]
        }

        response = self.client.post(
            path=reverse('purchase_order_creation'),
            data=request_data,
            format='json'
        )
        response_data = response.data

        self.assertEqual(response.status_code, 201)
        self.assertIsNotNone(response_data['supplier']['id'])
        self.assertEqual(request_data["supplier"]["name"], response_data["supplier"]["name"])
        self.assertEqual(request_data["supplier"]["email"], response_data["supplier"]["email"])
        self.assertEqual(len(request_data["line_items"]), len(response_data["line_items"]))
        self.assertEqual(response_data["total_tax"], "0.50")
        self.assertEqual(response_data["total_amount"], "10.50")
        self.assertEqual(response_data["total_quantity"], 1)

    def test_purchase_order_creation_request_for_existing_supplier(self):
        request_data = {
            "supplier": {
                "id": self.supplier.id,
                "name": "my supplier",
                "email": "email@email.com"
            },
            "line_items": [
                {
                  "item_name": "test prod",
                  "quantity": 1,
                  "price_without_tax": "10.00",
                  "tax_name": "GST 5%",
                  "tax_amount": "0.50"
                }
            ]
        }
        self.assertNotEqual(self.supplier.email, request_data["supplier"]["email"])

        response = self.client.post(
            path=reverse('purchase_order_creation'),
            data=request_data,
            format='json'
        )
        response_data = response.data
        self.supplier.refresh_from_db()

        self.assertEqual(response.status_code, 201)
        self.assertIsNotNone(response_data['supplier']['id'])
        self.assertEqual(response_data['supplier']['id'], self.supplier.id)
        self.assertEqual(self.supplier.name, response_data["supplier"]["name"])
        self.assertEqual(self.supplier.name, request_data["supplier"]["name"])
        self.assertEqual(self.supplier.email, response_data["supplier"]["email"])
        self.assertEqual(len(request_data["line_items"]), len(response_data["line_items"]))
        self.assertEqual(response_data["total_tax"], "0.50")
        self.assertEqual(response_data["total_amount"], "10.50")
        self.assertEqual(response_data["total_quantity"], 1)

    def test_purchase_order_get_request_by_id(self):
        response = self.client.get(
            path=reverse('purchase_order_view', kwargs={'purchase_order_id': self.purchase_order.id}),
        )
        response_data = response.data

        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.supplier.id, response_data["supplier"]["id"])
        self.assertEqual(self.supplier.name, response_data["supplier"]["name"])
        self.assertEqual(self.supplier.email, response_data["supplier"]["email"])
        self.assertEqual(len(self.line_items), len(response_data["line_items"]))
        self.assertEqual(response_data["total_tax"], "1.00")
        self.assertEqual(response_data["total_amount"], "5.00")
        self.assertEqual(response_data["total_quantity"], 4)

    def test_purchase_order_get_request_by_invalid_id(self):
        response = self.client.get(
            path=reverse('purchase_order_view', kwargs={'purchase_order_id': 9999}),
        )
        response_data = response.data

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response_data["error"], "Purchase id not found for id 9999")

    def test_purchase_order_delete_request_by_id(self):
        response = self.client.delete(
            path=reverse('purchase_order_view', kwargs={'purchase_order_id': self.purchase_order.id}),
        )

        self.assertEqual(response.status_code, 204)

    def test_purchase_order_delete_request_by_invalid_id(self):
        response = self.client.delete(
            path=reverse('purchase_order_view', kwargs={'purchase_order_id': 9999}),
        )
        response_data = response.data

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response_data["error"], "Purchase id not found for id 9999")

    def test_purchase_order_update_request_with_invalid_purchase_id(self):
        request_data = {
            "id": "999",
            "supplier": {
                "id": self.supplier.id,
                "name": "another supplier",
                "email": "email@email.com"
            },
            "line_items": [
                {
                    "id": self.line_items[0].id,
                    "item_name": "test prod",
                    "quantity": 1,
                    "price_without_tax": "10.00",
                    "tax_name": "GST 5%",
                    "tax_amount": "0.50"
                },
                {
                    "item_name": "new prod",
                    "quantity": 4,
                    "price_without_tax": "6.00",
                    "tax_name": "GST 5%",
                    "tax_amount": "0.30"
                }
            ]
        }
        response = self.client.put(
            path=reverse('purchase_order_view', kwargs={'purchase_order_id': 999}),
            data=request_data,
            format='json'
        )
        response_data = response.data

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response_data["error"], "Purchase id not found for id 999")

    def test_purchase_order_update_request_with_valid_data(self):
        existing_line_item_ids = [line_item.id for line_item in self.line_items]
        request_data = {
            "id": self.purchase_order.id,
            "supplier": {
                "id": self.supplier.id,
                "name": "another supplier",
                "email": "email@email.com"
            },
            "line_items": [
                {
                    "id": self.line_items[0].id,
                    "item_name": "test prod",
                    "quantity": 1,
                    "price_without_tax": "10.00",
                    "tax_name": "GST 5%",
                    "tax_amount": "0.50"
                },
                {
                    "item_name": "new prod",
                    "quantity": 4,
                    "price_without_tax": "6.00",
                    "tax_name": "GST 5%",
                    "tax_amount": "0.30"
                }
            ]
        }
        response = self.client.put(
            path=reverse('purchase_order_view', kwargs={'purchase_order_id': self.purchase_order.id}),
            data=request_data,
            format='json'
        )
        response_data = response.data
        line_item_updated_from_request = None
        line_item_created_from_request = None
        for line_item in response_data["line_items"]:
            if line_item["id"] == self.line_items[0].id:
                line_item_updated_from_request = line_item
            else:
                line_item_created_from_request = line_item

        self.assertEqual(response.status_code, 200)
        # asset state before update
        self.assertNotEqual(response_data["supplier"]['name'], self.supplier.name)
        self.assertNotEqual(response_data["supplier"]['email'], self.supplier.email)
        self.assertNotEqual(line_item_updated_from_request["item_name"], self.line_items[0].item_name)
        self.assertNotIn(line_item_created_from_request["id"], existing_line_item_ids)
        self.assertNotEqual(response_data["total_quantity"], self.purchase_order.total_quantity)
        self.assertNotEqual(response_data["total_tax"], self.purchase_order.total_tax)
        self.assertNotEqual(response_data["total_amount"], self.purchase_order.total_amount)
        # assert state after updated

        # update the objects
        self.supplier.refresh_from_db()
        self.purchase_order.refresh_from_db()
        line_item_queryset_after_update = LineItem.objects.filter(purchase_order=self.purchase_order)
        line_item_ids_after_update = line_item_queryset_after_update.values_list('id', flat=True)

        self.assertEqual(response_data["supplier"]['name'], self.supplier.name)
        self.assertEqual(response_data["supplier"]['email'], self.supplier.email)
        self.assertIn(line_item_created_from_request["id"], line_item_ids_after_update)
        self.assertEqual(response_data["total_quantity"], self.purchase_order.total_quantity)
        self.assertEqual(response_data["total_tax"], str(self.purchase_order.total_tax))
        self.assertEqual(response_data["total_amount"], str(self.purchase_order.total_amount))


    def test_get_purchase_order_with_supplier_name_query_param(self):
        response = self.client.get(
            path=reverse('purchase_order_creation'),
            **{'supplier_name': f'{self.supplier.name[0:2]}'}
        )
        response_data = response.data

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response_data),1)
        self.assertEqual(self.supplier.id, response_data[0]["supplier"]["id"])
        self.assertEqual(self.supplier.name, response_data[0]["supplier"]["name"])
        self.assertEqual(self.supplier.email, response_data[0]["supplier"]["email"])
        self.assertEqual(len(self.line_items), len(response_data[0]["line_items"]))
        self.assertEqual(response_data[0]["total_tax"], "1.00")
        self.assertEqual(response_data[0]["total_amount"], "5.00")
        self.assertEqual(response_data[0]["total_quantity"], 4)


    def test_get_purchase_order_with_line_item_name_query_param(self):
        response = self.client.get(
            path=reverse('purchase_order_creation'),
            **{'item_name': f'{self.line_items[0].item_name[0:2]}'}
        )
        response_data = response.data

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response_data),1)
        self.assertEqual(self.supplier.id, response_data[0]["supplier"]["id"])
        self.assertEqual(self.supplier.name, response_data[0]["supplier"]["name"])
        self.assertEqual(self.supplier.email, response_data[0]["supplier"]["email"])
        self.assertEqual(len(self.line_items), len(response_data[0]["line_items"]))
        self.assertEqual(response_data[0]["total_tax"], "1.00")
        self.assertEqual(response_data[0]["total_amount"], "5.00")
        self.assertEqual(response_data[0]["total_quantity"], 4)
