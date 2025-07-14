from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from users.models import User


class UserTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="test@example.com", password="strongpassword"
        )
        self.token_url = reverse("jwt-create")
        self.register_url = reverse("register")
        self.profile_url = reverse("profile")

    def test_user_registration(self):
        response = self.client.post(
            self.register_url,
            {"email": "newuser@example.com", "password": "newpassword123"},
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(email="newuser@example.com").exists())

    def test_jwt_token_generation(self):
        response = self.client.post(
            self.token_url, {"email": "test@example.com", "password": "strongpassword"}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_profile_authenticated_access(self):
        token = self.client.post(
            self.token_url, {"email": "test@example.com", "password": "strongpassword"}
        ).data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], "test@example.com")

    def test_profile_unauthenticated_access(self):
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
