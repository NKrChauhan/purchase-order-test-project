class PurchaseOrderNotFound(Exception):
    def __init__(self, purchase_order_id):
        self.error = f"Purchase id not found for id {purchase_order_id}"
