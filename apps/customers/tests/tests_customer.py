import json

from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_api_key.models import APIKey

from apps.addresses.models.address import Address
from apps.customers.models.customer import Customer
from apps.users.choices.roles_choices import RoleChoices
from apps.users.models.user import User


class CustomerViewTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.url_base = "/customers/"

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

        self.customer = Customer.objects.create(
            user=self.user_customer,
            phone_number="123456789",
            current_location=self.address
        )

    def get_token(self, user):
        return str(TokenObtainPairSerializer.get_token(user).access_token)

    def test_retrieve_customer_success(self):
        token = self.get_token(self.user_driver)
        response = self.client.get(
            f"{self.url_base}{self.customer.id}/",
            HTTP_X_API_KEY=self.api_key,
            HTTP_AUTHORIZATION=f"Bearer {token}",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["user"]["email"], "customer@example.com")

    def test_update_customer_success(self):
        token = self.get_token(self.user_driver)
        new_address = Address.objects.create(
            street="456 New St", latitude=15.0, longitude=25.0
        )
        payload = {
            "phone_number": "9876543210",
            "address": str(new_address.id)
        }
        response = self.client.put(
            f"{self.url_base}{self.customer.id}/",
            data=json.dumps(payload),
            content_type="application/json",
            HTTP_X_API_KEY=self.api_key,
            HTTP_AUTHORIZATION=f"Bearer {token}",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["phone_number"], "9876543210")

    def test_partial_update_customer_success(self):
        token = self.get_token(self.user_driver)
        payload = {
            "phone_number": "5555555555"
        }
        response = self.client.patch(
            f"{self.url_base}{self.customer.id}/",
            data=json.dumps(payload),
            content_type="application/json",
            HTTP_X_API_KEY=self.api_key,
            HTTP_AUTHORIZATION=f"Bearer {token}",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["phone_number"], "5555555555")

    def test_list_customers_success(self):
        token = self.get_token(self.user_driver)
        response = self.client.get(
            self.url_base,
            HTTP_X_API_KEY=self.api_key,
            HTTP_AUTHORIZATION=f"Bearer {token}",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data["results"]), 1)

    def test_delete_customer_success(self):
        token = self.get_token(self.user_driver)
        response = self.client.delete(
            f"{self.url_base}{self.customer.id}/",
            HTTP_X_API_KEY=self.api_key,
            HTTP_AUTHORIZATION=f"Bearer {token}",
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Customer.objects.filter(id=self.customer.id).exists())
