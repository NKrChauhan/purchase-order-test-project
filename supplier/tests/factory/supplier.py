import factory
from faker import Faker

from supplier.model.supplier import Supplier

fake = Faker()


class SupplierFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Supplier

    name = fake.name()
    email = fake.email()
