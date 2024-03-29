from ..model.supplier import Supplier
from ..serializers.supplier import SupplierSerializer


class SupplierService:
    """
        Service class for handling operations related to the Supplier model.

        Methods:
        - get_by_id(supplier_id)
        - get_by_name(supplier_name_regex)
        - create(name, email)
        - update_or_create(supplier_id, name, email)
        - get_serialized_supplier_object(supplier)
        - get_by_name_and_email(name, email)
    """

    def get_by_id(self, supplier_id):
        """
        Retrieves a Supplier instance by its ID.
        """
        try:
            supplier = Supplier.objects.get(id=supplier_id)
        except Supplier.DoesNotExist:
            # we can add logs or raise the custom errors
            supplier = None
        return supplier

    def get_by_name(self, supplier_name_regex):
        """
        Retrieves Supplier instances by a name regex pattern.
        """
        suppliers = Supplier.objects.filter(name__icontians=supplier_name_regex)
        return suppliers

    def create(self, name, email):
        """
        Creates a new Supplier instance.
        """
        supplier_object = Supplier.objects.create(name=name, email=email)
        return supplier_object

    def update_or_create(self, supplier_id, name, email):
        """
        Updates or creates a Supplier instance.
        """
        supplier = self.get_by_id(supplier_id) or self.get_by_name_and_email(name, email)
        if supplier:
            supplier.name = name
            supplier.email = email
            supplier.save()
        else:
            supplier = self.create(email=email, name=name)
        return supplier

    def get_serialized_supplier_object(self, supplier):
        """
        Returns serialized Supplier data.
        """
        return SupplierSerializer(supplier).data

    def get_by_name_and_email(self, name, email):
        """
        Retrieves a Supplier instance by name and email.
        """
        supplier = Supplier.objects.filter(name=name, email=email).first()
        return supplier
