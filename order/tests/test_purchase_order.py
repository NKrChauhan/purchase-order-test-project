from django.urls import reverse
from rest_framework.test import APITestCase


class PurchaseOrderViewTest(APITestCase):
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
