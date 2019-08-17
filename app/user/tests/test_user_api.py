from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')
ME_URL = reverse('user:me')


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    """Test the users API (public)"""

    def setUp(self) -> None:
        self.client = APIClient()
        self.payload = {
            "email": "user1@gmail.com",
            "password": "Admin@123",
        }

    def test_create_valid_user_success(self):
        """Test creating user with valid payload is successful"""
        response = self.client.post(CREATE_USER_URL, self.payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**response.data)
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
        user_exists = get_user_model().objects.filter(email=self.payload["email"]).exists()
        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        """Test that a token is created for user"""
        create_user(**self.payload)
        response = self.client.post(TOKEN_URL, self.payload)
        self.assertIn('access', response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_creds(self):
        """Test that the token is not created if the cres given are invalid"""
        create_user(**self.payload)
        self.payload["password"] = "pw"
        response = self.client.post(TOKEN_URL, **self.payload)
        self.assertNotIn("access", response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_no_user(self):
        response = self.client.post(TOKEN_URL, **self.payload)
        self.assertNotIn("access", response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_missing_input_field(self):
        """Test that email and password are required"""
        self.payload["password"] = None
        response = self.client.post(TOKEN_URL, **self.payload)
        self.assertNotIn("access", response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_user_unauthorized(self):
        """Test that user authentication is required for users"""
        response = self.client.get(ME_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserApiTests(TestCase):
    """Test api requests that require authentication"""

    def setUp(self) -> None:
        self.payload = {
            "email": "user1@gmail.com",
            "password": "Admin@123",
        }
        self.user = create_user(**self.payload)
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_profile_success(self):
        """Test retrieveing profile for a logged in user"""
        response = self.client.get(ME_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotIn("password", response.data)

    def test_post_me_not_allowed(self):
        """test that post is not allowed on the ME_URL"""
        input = {}
        response = self.client.post(ME_URL, input)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile(self):
        """Test updating the user profile for authenticated user"""
        payload = {"first_name": "kasper", "last_name": "spark"}
        response = self.client.patch(ME_URL, payload)

        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, payload["first_name"])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
