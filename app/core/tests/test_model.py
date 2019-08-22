from django.test import TestCase
from django.contrib.auth import get_user_model
from unittest.mock import patch
from core.models import Tag, Ingredient, Recipe, recipe_image_file_path


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class ModelTests(TestCase):

    def setUp(self) -> None:
        self.payload = {
            "email": "user1@gmail.com",
            "password": "Admin@123",
        }

    def test_tag_str(self):
        """Test the tag string representation"""
        tag_name = "vegan"
        tag = Tag.objects.create(user=create_user(**self.payload), name=tag_name)
        self.assertEqual(str(tag), tag_name)

    def test_ingredient_str(self):
        """Test ingredient string representation"""
        ingredient_name = "cucumber"
        ingredient = Ingredient.objects.create(user=create_user(**self.payload), name=ingredient_name)
        self.assertEqual(str(ingredient), ingredient_name)

    def test_recipe_str(self):
        """Test the recipe string representation"""
        recipe = Recipe.objects.create(
            user=create_user(**self.payload),
            title="Steak and mushroom sauce",
            time_minutes=5,
            price=5.00
        )
        self.assertEqual(str(recipe), recipe.title)

    @patch("uuid.uuid4")
    def test_recipe_file_name_uuid(self, mock_uuid):
        """Test that image is saved in the current location"""
        uuid = "test_uuid"
        mock_uuid.return_value = uuid
        filepath = recipe_image_file_path(None, "my_image.jpg")

        expected = f"uploads/recipe/{uuid}.jpg"
        self.assertEqual(str(filepath), expected)