class LineItemNotFound(Exception):
    def __init__(self, line_item_id):
        message = f"Purchase id not found for id {line_item_id}"
