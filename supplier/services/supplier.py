from ..model.supplier import Supplier
from ..serializers.supplier import SupplierSerializer


class SupplierService:
    def get_by_id(self, supplier_id):
        try:
            supplier = Supplier.objects.get(id=supplier_id)
        except Supplier.DoesNotExist:
            # we can add logs or raise the custom errors
            supplier = None
        return supplier

    def get_by_name(self, supplier_name_regex):
        suppliers = Supplier.objects.filter(name__icontians=supplier_name_regex)
        return suppliers

    def create(self, name, email):
        supplier_object = Supplier.objects.create(name=name, email=email)
        return supplier_object

    def update_or_create(self, supplier_id, name, email):
        supplier = self.get_by_id(supplier_id) or self.get_by_name_and_email(name, email)
        if supplier:
            # we can further optimise the save if we can get the supplier by
            supplier.name = name
            supplier.email = email
            supplier.save()
        else:
            supplier = self.create(email=email, name=name)
        return supplier

    def get_serialized_supplier_object(self, supplier):
        return SupplierSerializer(supplier).data

    def get_by_name_and_email(self, name, email):
        supplier = Supplier.objects.filter(name=name, email=email).first()
        return supplier
