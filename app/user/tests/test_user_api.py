from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse('user:create')


def create_user(**params):
    return get_user_model().objects.create_user(**params)

class PublicUserApiTests(TestCase):
    """Test the users API (public)"""

    def setUp(self) -> None:
        self.client = APIClient()
        self.payload = {
            "username":"user1",
            "email":"user1@gmail.com",
            "password":"Admin@123",
        }

    def test_create_valid_user_success(self):
        """Test creating user with valid payload is successful"""
        response = self.client.post(CREATE_USER_URL, self.payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user= get_user_model().objects.get(**response.data)
        self.assertTrue(user.check_password(self.payload["password"]))
        self.assertNotIn("password", response.data)


    def test_user_exists(self):
        """Test to create user that already exists"""
        create_user(**self.payload)
        response = self.client.post(CREATE_USER_URL, self.payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_password_min_length(self):
        """Test for min password length"""
        self.payload["password"] = "pw"
        response = self.client.post(CREATE_USER_URL, self.payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(email = self.payload["email"]).exists()
        self.assertFalse(user_exists)