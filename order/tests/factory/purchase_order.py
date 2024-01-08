import factory
from faker import Faker

from order.models.purchase_order import PurchaseOrder

fake = Faker()


class PurchaseOrderFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = PurchaseOrder

    supplier = factory.SubFactory('supplier.tests.factory.supplier.SupplierFactory')
    order_time = fake.date_time_this_decade()
    total_quantity = fake.random_int(min=1, max=1000)
    total_amount = fake.pydecimal(left_digits=4, right_digits=2, positive=True)
    total_tax = fake.pydecimal(left_digits=2, right_digits=2, positive=True)
