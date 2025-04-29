from rest_framework import serializers

from apps.drivers.models.driver import Driver


class DriverSerializer(serializers.ModelSerializer):
    """
    Serializer for retrieving and listing drivers.
    """

    full_name = serializers.CharField()

    class Meta:
        model = Driver
        fields = ("id", "phone_number", "email", "is_available", "current_location")
        read_only_fields = ("id", "is_available")
