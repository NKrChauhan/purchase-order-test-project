from django.contrib import admin

# Register your models here.
from order.models.purchase_order import PurchaseOrder

admin.site.register(PurchaseOrder)
