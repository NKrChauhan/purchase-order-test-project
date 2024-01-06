from django.db import models
from django.utils import timezone

from supplier.model.supplier import Supplier


class PurchaseOrder(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, help_text="Supplier of Order")
    order_time = models.DateTimeField(default=timezone.now, editable=False)
    order_number = models.IntegerField(unique=True, editable=False, null=True)
    total_quantity = models.IntegerField(editable=False)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    total_tax = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        super(PurchaseOrder, self).save(*args, **kwargs)
        if not self.order_number:
            self.order_number = self.pk
            super().save()

    class Meta:
        db_table = "purchase_orders"
        verbose_name = "Purchase Order"
        verbose_name_plural = "Purchase Orders"
