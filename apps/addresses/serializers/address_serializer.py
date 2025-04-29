# apps/addresses/serializers/address_serializer.py

from rest_framework import serializers

from apps.addresses.models.address import Address


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ("id", "street", "latitude", "longitude")


class AddressCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ("street", "latitude", "longitude")
