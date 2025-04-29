# apps/yourapp/management/commands/create_fake_data.py

from django.core.management.base import BaseCommand
from faker import Faker

from apps.addresses.models.address import Address
from apps.drivers.models.driver import Driver
from apps.users.choices.roles_choices import RoleChoices
from apps.users.models.user import User


class Command(BaseCommand):
    help = "Crea datos falsos para conductores y direcciones"

    def handle(self, *args, **kwargs):
        fake = Faker()

        addresses = []

        for _ in range(20):
            address = Address.objects.create(
                street=fake.street_address(),
                latitude=fake.latitude(),
                longitude=fake.longitude(),
            )
            addresses.append(address)

        for _ in range(20):
            user = User.objects.create_user(
                email=fake.unique.email(),
                password="password123",
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                role=RoleChoices.DRIVER,
            )
            Driver.objects.create(
                user=user,
                phone_number=fake.unique.numerify(text="##########"),
                current_location=fake.random_element(addresses),
                is_available=fake.boolean(),
            )

        self.stdout.write(self.style.SUCCESS("Datos falsos creados correctamente"))
