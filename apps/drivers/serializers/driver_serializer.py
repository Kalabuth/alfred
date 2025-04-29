from rest_framework import serializers

from apps.users.serializers.user_serializer import UserSerializer
from apps.drivers.models.driver import Driver


class DriverSerializer(serializers.ModelSerializer):
    """
    Serializer for retrieving and listing drivers.
    """
    user = UserSerializer() 

    class Meta:
        model = Driver
        fields = ("id", "phone_number", "is_available", "current_location", "user")
        read_only_fields = ("id", "is_available")
