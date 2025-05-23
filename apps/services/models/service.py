from django.db.models import CASCADE, SET_NULL, CharField, ForeignKey, IntegerField

from apps.customers.models.customer import Customer
from apps.addresses.models.address import Address
from apps.common.models.base_model import BaseModel
from apps.drivers.models.driver import Driver
from apps.services.choices.status_service import ServiceStatus


class Service(BaseModel):
    client_address = ForeignKey(
        Address, related_name="client_services", on_delete=CASCADE
    )
    driver = ForeignKey(Driver, on_delete=SET_NULL, null=True, blank=True)
    status = CharField(choices=ServiceStatus.choices, default=ServiceStatus.PENDING[0])
    estimated_time_minutes = IntegerField(null=True, blank=True)
    customer = ForeignKey(Customer, on_delete=SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Service #{self.id} - {self.status}"
