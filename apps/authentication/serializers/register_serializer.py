from rest_framework import serializers

from apps.customers.models.customer import Customer
from apps.drivers.models.driver import Driver
from apps.users.choices.roles_choices import RoleChoices
from apps.users.models.user import User


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    phone_number = serializers.CharField(required=False)
    current_location_id = serializers.UUIDField(required=True)

    class Meta:
        model = User
        fields = [
            "email",
            "password",
            "first_name",
            "last_name",
            "role",
            "phone_number",
            "current_location_id",
        ]

    def create(self, validated_data):
        password = validated_data.pop("password")
        role = validated_data.pop("role")
        phone_number = validated_data.pop("phone_number", None)
        current_location_id = validated_data.pop("current_location_id", None)

        user = User(**validated_data)
        user.set_password(password)
        user.role = role
        user.save()

        if role == RoleChoices.DRIVER:
            Driver.objects.create(
                user=user,
                phone_number=phone_number,
                current_location_id=current_location_id,
            )
        elif role == RoleChoices.CUSTOMER:
            Customer.objects.create(
                user=user,
                phone_number=phone_number,
                current_location_id=current_location_id,
            )

        return user
