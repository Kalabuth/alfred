import json

from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from apps.addresses.models.address import Address
from apps.users.choices.roles_choices import RoleChoices
from apps.users.models.user import User
from rest_framework_api_key.models import APIKey


class AddressViewTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.url_base = "/address/"

        self.user_customer = User.objects.create_user(
            email="customer@example.com",
            password="testpassword",
            role=RoleChoices.CUSTOMER,
        )
        self.user_driver = User.objects.create_user(
            email="driver@example.com",
            password="testpassword",
            role=RoleChoices.DRIVER,
        )

        _, self.api_key = APIKey.objects.create_key(name="test")

        self.address = Address.objects.create(
            street="123 Main St", latitude=10.0, longitude=20.0
        )

    def get_token(self, user):
        return str(TokenObtainPairSerializer.get_token(user).access_token)

    def test_create_address_success(self):
        token = self.get_token(self.user_driver)
        payload = {"street": "456 Elm St", "latitude": 15.0, "longitude": 25.0}
        response = self.client.post(
            self.url_base,
            data=json.dumps(payload),
            content_type="application/json",
            HTTP_X_API_KEY=self.api_key,
            HTTP_AUTHORIZATION=f"Bearer {token}",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["street"], "456 Elm St")

    def test_create_address_invalid_data(self):
        token = self.get_token(self.user_driver)
        payload = {"street": "", "latitude": "not_a_number", "longitude": None}
        response = self.client.post(
            self.url_base,
            data=json.dumps(payload),
            content_type="application/json",
            HTTP_X_API_KEY=self.api_key,
            HTTP_AUTHORIZATION=f"Bearer {token}",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_address_success(self):
        token = self.get_token(self.user_driver)
        response = self.client.get(
            f"{self.url_base}{self.address.id}/",
            HTTP_X_API_KEY=self.api_key,
            HTTP_AUTHORIZATION=f"Bearer {token}",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["street"], "123 Main St")

    def test_update_address_success(self):
        token = self.get_token(self.user_driver)
        payload = {"street": "Updated Street", "latitude": 30.0, "longitude": 40.0}
        response = self.client.put(
            f"{self.url_base}{self.address.id}/",
            data=json.dumps(payload),
            content_type="application/json",
            HTTP_X_API_KEY=self.api_key,
            HTTP_AUTHORIZATION=f"Bearer {token}",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["street"], "Updated Street")

    def test_list_addresses_success(self):
        token = self.get_token(self.user_driver)
        Address.objects.create(street="789 Oak St", latitude=5.0, longitude=10.0)
        Address.objects.create(street="456 Pine St", latitude=7.5, longitude=12.5)
        response = self.client.get(
            self.url_base,
            HTTP_X_API_KEY=self.api_key,
            HTTP_AUTHORIZATION=f"Bearer {token}",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data["results"]), 3)
