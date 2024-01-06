from decimal import Decimal

from django.db import models

from order.models.purchase_order import PurchaseOrder


class LineItem(models.Model):
    item_name = models.CharField(max_length=256)
    quantity = models.IntegerField()
    price_without_tax = models.DecimalField(max_digits=10, decimal_places=2)
    tax_name = models.CharField(max_length=124)
    tax_total = models.DecimalField(max_digits=10, decimal_places=2)
    line_total = models.DecimalField(max_digits=10, decimal_places=2)
    purchase_order = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE, help_text="Purchase Order")

    def save(self, *args, **kwargs):
        self.line_total = Decimal(str(self.tax_total)) + Decimal(str(self.price_without_tax))
        super(LineItem, self).save(*args, **kwargs)

    class Meta:
        db_table = "line_items"
        verbose_name = "Line Item"
        verbose_name_plural = "Line Items"
