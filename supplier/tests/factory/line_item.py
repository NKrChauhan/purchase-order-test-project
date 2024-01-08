import factory
from faker import Faker

from supplier.model.line_items import LineItem

fake = Faker()


class LineItemFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = LineItem

    item_name = fake.word()
    quantity = fake.random_int(min=1, max=100)
    price_without_tax = fake.pydecimal(left_digits=3, right_digits=2, positive=True)
    tax_name = fake.word()
    tax_total = fake.pydecimal(left_digits=2, right_digits=2, positive=True)
    line_total = price_without_tax + tax_total
