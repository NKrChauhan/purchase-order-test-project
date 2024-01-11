# Sumtracker: Purchase order Project

## Getting Up and Running

Minimum requirements :
- Docker Engine version 23.0.6
- Docker Compose version v2.17.3

Go to the directory with Dockerfile & docker-compose.yaml file of the project and Run:
```bash
docker compose up
```

## CURLS for testing APIs

### DRF Spectacular docs
Go to the following url after running the server
```bash
  http://0.0.0.0:8000/docs/
```

### Create purchase order
POST /purchase/orders/
```bash
  curl --request POST \
    --url http://0.0.0.0:8000/purchase/orders/ \
    --header 'Content-Type: application/json' \
    --header 'User-Agent: insomnia/8.5.1' \
    --data '{
    "supplier": {
      "id": 17,
      "name": "mys supplier",
      "email": "email@email.com"
    },
    "line_items": [
      {
        "item_name": "test prod 1",
        "quantity": 1,
        "price_without_tax": "10.00",
        "tax_name": "GST 5%",
        "tax_amount": "0.50"
      }
    ]
  }'
```
### Get purchase order by purchase order id
GET /purchase/orders/<int:id>/
```bash
  curl --request GET \
    --url http://0.0.0.0:8000/purchase/orders/1/ \
    --header 'Content-Type: application/json' \
    --header 'User-Agent: insomnia/8.5.1'
```
### Delete purchase order by purchase order id
DELETE /purchase/orders/<int:id>/
```bash
  curl --request DELETE \
    --url http://0.0.0.0:8000/purchase/orders/1/ \
    --header 'Content-Type: application/json' \
    --header 'User-Agent: insomnia/8.5.1'
```
### Update purchase order by purchase order id
PUT /purchase/orders/<int:id>/
```bash
  curl --request PUT \
    --url http://0.0.0.0:8000/purchase/orders/2/ \
    --header 'Content-Type: application/json' \
    --header 'User-Agent: insomnia/8.5.1' \
    --data '{
      "id": 2,
      "supplier": {
          "id": 2,
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
  }'
```
### Get purchase orders by supplier_name query_param
GET /purchase/orders/?supplier_name=<str:supplier_name>
```bash
  curl --request GET \
    --url 'http://0.0.0.0:8000/purchase/orders/?supplier_name=my' \
    --header 'Content-Type: application/json' \
    --header 'User-Agent: insomnia/8.5.1'
```
### Get purchase orders by item_name query_param
GET /purchase/orders/?item_name=<str:item_name>
```bash
  curl --request GET \
    --url 'http://0.0.0.0:8000/purchase/orders/?item_name=prod' \
    --header 'Content-Type: application/json' \
    --header 'User-Agent: insomnia/8.5.1'
```
### Get all purchase orders
GET /purchase/orders/
```bash
  curl --request GET \
    --url http://0.0.0.0:8000/purchase/orders/ \
    --header 'Content-Type: application/json' \
    --header 'User-Agent: insomnia/8.5.1'
```

---
## Scope of improvements and enhancements
- Testing
  - In current codebase set up the unittests are written for views. 
  - tests for each service and api service can be added with even more test case scenarios.
- Authentication
  - currently, the api is not authenticated by any means
- Adding logger
  - adding logs to the critical parts such as while creation and updating the objects will be helpful in debugging the issue might occur in future
  - logs can be added at following parts:
    - view level
    - api service level
    - service level 

    for each app order & supplier(includes supplier and line_item)
