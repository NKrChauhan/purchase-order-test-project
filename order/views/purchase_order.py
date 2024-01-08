from rest_framework.response import Response
from rest_framework.views import APIView

from order.api_services.purchase_order import PurchaseOrderAPIService


class PurchaseOrderAPIView(APIView):
    purchase_order_api_service = PurchaseOrderAPIService()

    def get(self, request, purchase_order_id=None):
        """
        Retrieve a single Purchase Order if 'purchase_order_id' is provided,
        else return a list of Purchase Orders based on query_params if provided.
        """
        query_params = request.query_params
        # If Id is given in the url then that will take the precedence over the query_params
        try:
            if purchase_order_id:
                response_data = self.purchase_order_api_service.get_by_id(purchase_order_id=purchase_order_id)
            elif query_params:
                response_data = self.purchase_order_api_service.get_by_query_params(query_params=query_params)
            else:
                # if there is no purchase_order_id or query_params provided then return all purchase orders list
                response_data = self.purchase_order_api_service.get_all_purchase_orders()
        except Exception as e:
            return Response(status=400, data=e.__dict__)
        return Response(status=200, data=response_data)

    def post(self, request):
        """
        Create a new Purchase Order.
        request.data: {
            "supplier": {
                "id": null,
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
        """
        request_data = request.data
        try:
            saved_purchase_order_data = self.purchase_order_api_service.create(data=request_data)
        except Exception as e:
            return Response(status=400, data=e.__dict__)
        return Response(status=201, data=saved_purchase_order_data)

    def put(self, request, purchase_order_id):
        """
       Update a specific Purchase Order identified by 'purchase_order_id'.
       request.data: {
          "id": 3,
          "supplier": {
            "id": 15,
            "name": "another supplier",
            "email": "email@email.com"
          },
          "line_items": [
            {
              "id": 2,
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
       """
        request_data = request.data
        if purchase_order_id:
            try:
                updated_purchase_data = self.purchase_order_api_service.update(purchase_order_id=purchase_order_id, data=request_data)
            except Exception as e:
                return Response(status=400, data=e.__dict__)
        else:
            return Response(status=400, data={"error": "missing purchase id"})
        return Response(status=200, data=updated_purchase_data)

    def delete(self, request, purchase_order_id):
        """
        Delete a specific Purchase Order identified by 'purchase_order_id'.
        """
        if purchase_order_id:
            try:
                self.purchase_order_api_service.delete_by_id(purchase_order_id=purchase_order_id)
            except Exception as e:
                return Response(status=400, data=e.__dict__)
        else:
            return Response(status=400, data={"error": "missing purchase id"})
        return Response(status=204)
