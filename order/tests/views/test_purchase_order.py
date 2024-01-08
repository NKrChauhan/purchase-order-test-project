from django.urls import reverse
from rest_framework.test import APITestCase

from order.tests.factory.purchase_order import PurchaseOrderFactory
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
            size=2, purchase_order=self.purchase_order, quantity=2, price_without_tax=2.0, tax_total=0.5
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
            path=reverse('purchase_order_creation')+f'{self.purchase_order.id}/'
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
            path=reverse('purchase_order_creation')+'10/'
        )
        response_data = response.data

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_data["message"], "Purchase id not found for id 10")

    def test_purchase_order_delete_request_by_id(self):
        response = self.client.delete(
            path=reverse('purchase_order_creation')+f'{self.purchase_order.id}/'
        )

        self.assertEqual(response.status_code, 204)

    def test_purchase_order_delete_request_by_invalid_id(self):
        response = self.client.get(
            path=reverse('purchase_order_creation')+'10/'
        )
        response_data = response.data

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_data["message"], "Purchase id not found for id 10")
