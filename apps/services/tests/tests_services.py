import json
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_api_key.models import APIKey

from apps.customers.models.customer import Customer
from apps.users.models.user import User
from apps.users.choices.roles_choices import RoleChoices
from apps.addresses.models.address import Address
from apps.services.models.service import Service
from apps.drivers.models.driver import Driver
from apps.services.choices.status_service import ServiceStatus


class ServiceViewTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.url_base = "/service/"

        self.user_customer = User.objects.create_user(
            email="client@example.com",
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
            street="456 Customer St", latitude=10.0, longitude=20.0
        )
        self.customer = Customer.objects.create(
            user=self.user_customer,
            phone_number="123456789",
            current_location=self.address
        )
        self.driver = Driver.objects.create(
            user=self.user_driver,
            is_available=True,
            current_location=self.address
        )

        self.service = Service.objects.create(
            client_address=self.address,
            status=ServiceStatus.PENDING,
            customer=self.customer
        )

    def get_token(self, user):
        return str(TokenObtainPairSerializer.get_token(user).access_token)

    def test_list_services_success(self):
        token = self.get_token(self.user_customer)
        response = self.client.get(
            self.url_base,
            HTTP_X_API_KEY=self.api_key,
            HTTP_AUTHORIZATION=f"Bearer {token}",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data["results"]), 1)

    def test_create_service_success(self):
        token = self.get_token(self.user_customer)
        payload = {}
        response = self.client.post(
            self.url_base,
            data=json.dumps(payload),
            content_type="application/json",
            HTTP_X_API_KEY=self.api_key,
            HTTP_AUTHORIZATION=f"Bearer {token}",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_retrieve_service_success(self):
        token = self.get_token(self.user_customer)
        response = self.client.get(
            f"{self.url_base}{self.service.id}/",
            HTTP_X_API_KEY=self.api_key,
            HTTP_AUTHORIZATION=f"Bearer {token}",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], str(self.service.id))

    def test_retrieve_service_not_found(self):
        token = self.get_token(self.user_customer)
        fake_id = "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"
        response = self.client.get(
            f"{self.url_base}{fake_id}/",
            HTTP_X_API_KEY=self.api_key,
            HTTP_AUTHORIZATION=f"Bearer {token}",
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_complete_service_success(self):
        token = self.get_token(self.user_customer)
        self.service.status = ServiceStatus.IN_PROGRESS
        self.service.driver = self.driver
        self.service.save()

        response = self.client.post(
            f"{self.url_base}{self.service.id}/complete/",
            HTTP_X_API_KEY=self.api_key,
            HTTP_AUTHORIZATION=f"Bearer {token}",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.service.refresh_from_db()
        self.assertEqual(self.service.status, ServiceStatus.COMPLETED)

    def test_complete_service_invalid_status(self):
        token = self.get_token(self.user_customer)
        self.service.status = ServiceStatus.PENDING
        self.service.save()

        response = self.client.post(
            f"{self.url_base}{self.service.id}/complete/",
            HTTP_X_API_KEY=self.api_key,
            HTTP_AUTHORIZATION=f"Bearer {token}",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["detail"], "Only assigned services can be completed.")
