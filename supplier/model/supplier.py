from django.db import models


class Supplier(models.Model):
    name = models.CharField(max_length=256, blank=True)
    # considering email is not unique
    email = models.EmailField(max_length=256, null=False)

    class Meta:
        db_table = "suppliers"
        verbose_name = "Supplier"
        verbose_name_plural = "Suppliers"
