from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Tag
from recipe.serializers import TagSerializer

TAGS_URL = reverse('recipe:tag-list')


class PublicTagsApiTests(TestCase):
    """Test the public available tags API"""

    def setUp(self) -> None:
        self.client = APIClient()

    def test_login_required(self):
        """Test that login is required for retreiving tags"""
        response = self.client.get(TAGS_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTagsApiTests(TestCase):
    """Test the authorised user tags API"""

    def setUp(self) -> None:
        self.payload = {
            "email": "user1@gmail.com",
            "password": "Admin@123",
        }
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(**self.payload)
        self.client.force_authenticate(self.user)

    def test_retrieve_tags(self):
        """Test retrieving tags"""
        Tag.objects.create(user=self.user, name="vegan")
        Tag.objects.create(user=self.user, name="dessert")

        response = self.client.get(TAGS_URL)
        tags = Tag.objects.all().order_by("-name")

        serializer = TagSerializer(tags, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_tags_limited_to_authenticated_users(self):
        """Test that tags returned are for the authenticated user"""
        payload = self.payload
        payload["email"] = "user2@gmail.com"

        user2 = get_user_model().objects.create_user(**payload)
        Tag.objects.create(user=user2, name='fruity')
        tag = Tag.objects.create(user=self.user, name='dessert')

        response = self.client.get(TAGS_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["name"], tag.name)

    def test_create_tag_success(self):
        """Test createing a new tag """
        payload = {"name":"Testtag"}
        self.client.post(TAGS_URL, payload)
        exists = Tag.objects.filter(
            user=self.user,
            name=payload["name"]
        )
        self.assertTrue(exists)

    def test_create_tag_invalid(self):
        """Test createing a new tag """
        payload = {"name":""}
        response = self.client.post(TAGS_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)