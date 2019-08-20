from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status
from core.models import Recipe, Tag, Ingredient
from recipe.serializers import RecipeSerializer, RecipeDetailSerializer

RECIPE_URL = reverse("recipe:recipe-list")

def detail_url(recipe_id):
    """Return recipe detail url"""
    return reverse("recipe:recipe-detail", args=[recipe_id])

def sample_tag(user, name="main course"):
    """Create and return a sample tag"""
    return Tag.objects.create(user=user, name=name)

def sample_ingredient(user, name="cinnamon"):
    """Create and return a sample tag"""
    return Ingredient.objects.create(user=user, name=name)

def sample_recipe(user, **kwargs):
    """Create and return recipe"""
    defaults = {
        "title": "Sample Recipe",
        "time_minutes": 10,
        "price": 4.00,
    }
    defaults.update(kwargs)
    return Recipe.objects.create(user=user, **defaults)


class PublicRecipApiTests(TestCase):
    """Test unauthenticated recipe api access"""

    def setUp(self) -> None:
        self.client = APIClient()

    def test_auth_required(self):
        """Test that auth is required"""
        response = self.client.get(RECIPE_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateRecipeApiTests(TestCase):
    """Test authenticated recipe api access"""

    def setUp(self) -> None:
        self.recipe_payload = {
            "title": "Chocloate CheeseCake",
            "time_minutes": 30,
            "price": 3.99,
        }
        self.payload = {
            "email": "user1@gmail.com",
            "password": "Admin@123",
        }
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(**self.payload)
        self.client.force_authenticate(self.user)

    def test_retrieve_recipes(self):
        """Test retreieving a list of recipes"""
        sample_recipe(user=self.user)
        sample_recipe(user=self.user)

        response = self.client.get(RECIPE_URL)
        recipes = Recipe.objects.all().order_by("-id")
        serializer = RecipeSerializer(recipes, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_recipe_limited_to_user(self):
        """Test retrieving recipe for user"""
        payload = self.payload
        payload["email"] = "user2@gmail.com"

        user2 = get_user_model().objects.create_user(**payload)
        sample_recipe(user=user2)
        sample_recipe(user=self.user)

        response = self.client.get(RECIPE_URL)
        recipes = Recipe.objects.filter(user=self.user)
        serializer = RecipeSerializer(recipes, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data, serializer.data)

    def test_view_recipe_detail(self):
        """Test viewing a recipe detail"""
        recipe = sample_recipe(user=self.user)
        recipe.tags.add(sample_tag(user=self.user))
        recipe.ingredients.add(sample_ingredient(user=self.user))
        url = detail_url(recipe.id)
        response = self.client.get(url)
        serializer = RecipeDetailSerializer(recipe)
        self.assertEqual(response.data, serializer.data)

    def test_create_basic_recipe(self):
        """Test creating recipe"""
        response = self.client.post(RECIPE_URL, self.recipe_payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        recipe = Recipe.objects.get(id=response.data["id"])
        for key in self.recipe_payload.keys():
            self.assertEqual(str(self.recipe_payload[key]), str(recipe.__getattribute__(key)))

    def test_create_recipe_with_tags(self):
        """Test creating recipe with tags"""
        tag1 = sample_tag(user=self.user, name="vegan")
        tag2 = sample_tag(user=self.user, name="dessert")

        self.recipe_payload["tags"] = [tag1.id, tag2.id]
        response = self.client.post(RECIPE_URL, self.recipe_payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        recipe = Recipe.objects.get(id=response.data["id"])
        tags = recipe.tags.all()
        self.assertEqual(tags.count(), 2)
        self.assertIn(tag1, tags)
        self.assertIn(tag2, tags)

    def test_creaing_recipe_with_ingredient(self):
        """Test creating recipe with ingredients"""
        ingredient1 = sample_ingredient(user=self.user, name="prawns")
        ingredient2 = sample_ingredient(user=self.user, name="ginger")
        self.recipe_payload["ingredients"] = [ingredient1.id, ingredient2.id]
        response = self.client.post(RECIPE_URL, self.recipe_payload)
        recipe = Recipe.objects.get(id=response.data["id"])
        ingredients = recipe.ingredients.all()
        self.assertEqual(ingredients.count(), 2)
        self.assertIn(ingredient1, ingredients)
        self.assertIn(ingredient2, ingredients)
        print(RECIPE_URL)