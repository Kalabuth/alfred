from rest_framework import serializers

from apps.customers.models.customer import Customer


class CustomerSerializer(serializers.ModelSerializer):
    """
    Serializer para leer (GET) Customers
    """

    class Meta:
        model = Customer
        fields = [
            "id",
            "first_name",
            "last_name",
            "email",
            "phone",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]


class CustomerCreateSerializer(serializers.ModelSerializer):
    """
    Serializer para crear y actualizar (POST/PUT/PATCH) Customers
    """

    class Meta:
        model = Customer
        fields = [
            "first_name",
            "last_name",
            "email",
            "phone",
        ]
