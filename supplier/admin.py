from django.contrib import admin

# Register your models here.
from supplier.model.line_items import LineItem
from supplier.model.supplier import Supplier

admin.site.register(LineItem)
admin.site.register(Supplier)
