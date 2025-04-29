import json
import uuid

from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_api_key.models import APIKey

from apps.drivers.models.driver import Driver
from apps.addresses.models.address import Address
from apps.users.choices.roles_choices import RoleChoices
from apps.users.models.user import User


class DriverViewTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.url_base = "/drivers/"

        self.user_driver = User.objects.create_user(
            email="driver@example.com",
            password="testpassword",
            role=RoleChoices.DRIVER,
        )
        self.user_customer = User.objects.create_user(
            email="customer@example.com",
            password="testpassword",
            role=RoleChoices.CUSTOMER,
        )

        _, self.api_key = APIKey.objects.create_key(name="test")

        self.address = Address.objects.create(
            street="123 Main St", latitude=10.0, longitude=20.0
        )

        self.driver = Driver.objects.create(
            user=self.user_driver,
            is_available=True,
            current_location=self.address
        )

    def get_token(self, user):
        return str(TokenObtainPairSerializer.get_token(user).access_token)

    def test_list_drivers_success(self):
        token = self.get_token(self.user_driver)
        response = self.client.get(
            self.url_base,
            HTTP_X_API_KEY=self.api_key,
            HTTP_AUTHORIZATION=f"Bearer {token}",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_retrieve_driver_success(self):
        token = self.get_token(self.user_driver)
        response = self.client.get(
            f"{self.url_base}{self.driver.id}/",
            HTTP_X_API_KEY=self.api_key,
            HTTP_AUTHORIZATION=f"Bearer {token}",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["user"]["email"], "driver@example.com")

    def test_update_driver_availability_success(self):
        token = self.get_token(self.user_driver)
        payload = {"is_available": False}
        response = self.client.post(
            f"{self.url_base}{self.driver.id}/update_availability/",
            data=json.dumps(payload),
            content_type="application/json",
            HTTP_X_API_KEY=self.api_key,
            HTTP_AUTHORIZATION=f"Bearer {token}",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.driver.refresh_from_db()
        self.assertFalse(self.driver.is_available)

    def test_closest_drivers_success(self):
        client_address = Address.objects.create(
            street="456 Customer St", latitude=10.1, longitude=20.1
        )

        token = self.get_token(self.user_driver)
        response = self.client.get(
            f"{self.url_base}closest-drivers/{client_address.id}/",
            HTTP_X_API_KEY=self.api_key,
            HTTP_AUTHORIZATION=f"Bearer {token}",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)
        self.assertIn("driver_id", response.data[0])
        self.assertIn("distance_km", response.data[0])
        self.assertIn("estimated_arrival_time_min", response.data[0])

    def test_closest_drivers_address_not_found(self):
        token = self.get_token(self.user_driver)
        non_existent_uuid = uuid.uuid4()
        response = self.client.get(
            f"{self.url_base}closest/?address_id={non_existent_uuid}",
            HTTP_X_API_KEY=self.api_key,
            HTTP_AUTHORIZATION=f"Bearer {token}",
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

