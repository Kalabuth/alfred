from rest_framework import serializers

from apps.users.serializers.user_serializer import UserSerializer
from apps.addresses.models.address import Address
from apps.customers.models.customer import Customer


class CustomerSerializer(serializers.ModelSerializer):
    """
    Serializer to read (GET) Customers
    """
    user = UserSerializer() 
    class Meta:
        model = Customer
        fields = [
            "id",
            "phone_number",
            "created_at",
            "updated_at",
            "user"
        ]
        read_only_fields = ["id", "created_at", "updated_at"]


class CustomerCreateSerializer(serializers.ModelSerializer):
    """
    Serializer to create and update (POST/PUT/PATCH) Customers
    """

    class Meta:
        model = Customer
        fields = ["phone_number", "current_location"]

    def validate_current_location(self, value):
        if value:
            try:
                address = Address.objects.get(id=value)
            except Address.DoesNotExist:
                raise serializers.ValidationError("Address not found")
        return value
