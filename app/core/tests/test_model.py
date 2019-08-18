from django.test import TestCase
from django.contrib.auth import get_user_model

from core.models import Tag, Ingredient


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
        ingredient = Ingredient.objects.create(user = create_user(**self.payload), name=ingredient_name)
        self.assertEqual(str(ingredient), ingredient_name)