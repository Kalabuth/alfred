from django.db.models import (
    CASCADE,
    SET_NULL,
    CharField,
    DateTimeField,
    ForeignKey,
    OneToOneField,
)

from apps.addresses.models.address import Address
from apps.common.models.base_model import BaseModel
from apps.users.models.user import User


class Customer(BaseModel):
    user = OneToOneField(User, on_delete=CASCADE, related_name="customer")
    current_location = ForeignKey(Address, on_delete=SET_NULL, null=True)
    phone_number = CharField(max_length=20, blank=True, null=True)
    created_at = DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Customer: {self.user.full_name or self.user.email}"
