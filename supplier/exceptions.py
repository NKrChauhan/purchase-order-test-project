class LineItemNotFound(Exception):
    def __init__(self, line_item_id):
        self.message = f"Line Item id not found for id {line_item_id}"
