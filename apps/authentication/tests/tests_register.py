from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model

from apps.addresses.models.address import Address

class AuthenticationViewTests(APITestCase):

    def test_register_user(self):
        address = Address.objects.create(
            street="123 Main St", latitude=10.0, longitude=20.0
        )
        data = {
            "email": "testuser@example.com",
            "password": "securepassword123",
            "first_name": "Test",
            "last_name": "User",
            "role": "customer",
            "current_location_id": address.id,
        }

        response = self.client.post('/auth/register/', data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

        User = get_user_model()
        user = User.objects.get(email=data['email'])
        self.assertEqual(user.first_name, data['first_name'])
        self.assertEqual(user.last_name, data['last_name'])

