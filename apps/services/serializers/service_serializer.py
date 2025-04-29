from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from apps.services.choices.status_service import ServiceStatus
from apps.services.models.service import Service


class ServiceSerializer(serializers.ModelSerializer):
    """
    Serializer for retrieving and listing services.
    """

    class Meta:
        model = Service
        fields = ("id", "client_address", "driver", "status", "estimated_time_minutes")


class ServiceCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating a new service using the logged-in customer's address.
    """

    class Meta:
        model = Service
        fields = ()

    def create(self, validated_data):
        user = self.context["request"].user

        customer = user.customer

        if not customer.current_location:
            raise ValidationError("Customer does not have a registered address.")

        service = Service.objects.create(
            client_address=customer.current_location,
            status=ServiceStatus.PENDING,
        )

        return service
