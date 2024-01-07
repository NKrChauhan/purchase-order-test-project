class PurchaseOrderNotFound(Exception):
    def __init__(self, purchase_order_id):
        message = f"Purchase id not found for id {purchase_order_id}"
