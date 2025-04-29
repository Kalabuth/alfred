from django.db.models import (
    CASCADE,
    SET_NULL,
    BooleanField,
    CharField,
    ForeignKey,
    OneToOneField,
)

from apps.addresses.models.address import Address
from apps.common.models.base_model import BaseModel
from apps.users.models.user import User


class Driver(BaseModel):
    user = OneToOneField(User, on_delete=CASCADE, related_name="driver")
    phone_number = CharField(max_length=20, unique=True, null=True, blank=True)
    current_location = ForeignKey(Address, on_delete=SET_NULL, null=True, blank=True)
    is_available = BooleanField(default=True)

    def __str__(self):
        return self.id
