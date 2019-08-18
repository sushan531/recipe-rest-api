from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Ingredient
from recipe.serializers import IngredientSerializer

INGREDIENT_URL = reverse("recipe:ingredient-list")


class PublicIngredientsApiTests(TestCase):
    """Test the publicly available ingredients API"""

    def setUp(self) -> None:
        self.client = APIClient()

    def test_login_required(self):
        """Test that login is required to access the endpoint"""
        response = self.client.get(INGREDIENT_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateIngredientApiTests(TestCase):
    """Test the private ingredients api"""

    def setUp(self) -> None:
        self.payload = {
            "email": "user1@gmail.com",
            "password": "Admin@123",
        }
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(**self.payload)
        self.client.force_authenticate(self.user)

    def test_retreive_ingredient_list(self):
        """Test retreiving a list of ingredients"""
        Ingredient.objects.create(user=self.user, name="kale")
        Ingredient.objects.create(user=self.user, name="sale")

        response = self.client.get(INGREDIENT_URL)

        ingredients = Ingredient.objects.all().order_by("-name")
        serializer = IngredientSerializer(ingredients, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_ingredient_limited_to_user(self):
        """Test that ingredients for the authenticated user are returned"""
        payload = self.payload
        payload["email"] = "user2@gmail.com"
        user2 = get_user_model().objects.create_user(**payload)
        Ingredient.objects.create(user=user2, name="vinegar")

        ingredient = Ingredient.objects.create(user=self.user, name="turmeric")

        response = self.client.get(INGREDIENT_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["name"], ingredient.name)

    def test_creata_ingredient_success(self):
        payload = {"name": "cabbage"}
        self.client.post(INGREDIENT_URL, payload)
        exists = Ingredient.objects.filter(user=self.user, name=payload["name"]).exists()
        self.assertTrue(exists)

    def test_creating_ingredient_invalid(self):
        """testing creating invalid ingredinet failed"""
        payload = {"name": ""}
        response = self.client.post(INGREDIENT_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)