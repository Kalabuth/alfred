from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model

class AuthenticationViewTests(APITestCase):

    def setUp(self):
        self.user_data = {
            "email": "testuser@example.com",
            "password": "securepassword123",
            "first_name": "Test",
            "last_name": "User"
        }
        self.user = get_user_model().objects.create_user(**self.user_data)

    def test_login_user_success(self):
        data = {
            "email": self.user_data['email'],
            "password": self.user_data['password']
        }

        response = self.client.post('/auth/login/', data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_login_user_invalid_credentials(self):
        data = {
            "email": "wronguser@example.com",
            "password": "wrongpassword123"
        }

        response = self.client.post('/auth/login/', data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertEqual(response.data, {"detail": "Invalid credentials."})
