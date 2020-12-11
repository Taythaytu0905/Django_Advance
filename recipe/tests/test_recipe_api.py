from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from core.models import Recipe
from recipe.serializers import RecipeSerializer

RECIPES_URL = reverse('recipe:recipe-list')


def sample_recipe(user, **params):
    """Create and return a sample recipe"""
    defaults = {
        'title': 'Sample recipe',
        'time_minutes': 10,
        'price': 5.00
    }
    defaults.update(params)
    return Recipe.objects.create(user=user, **defaults)


class PublicRecipesApiTests(TestCase):
    """Test the public available recipes API"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login is required for retrieving recipes"""
        res = self.client.get(RECIPES_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateRecipesApiTests(TestCase):
    """Test the authorized user recipe API"""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            'do@gmail.com', 'testpass')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_recipes(self):
        """Test retrieving recipe"""
        sample_recipe(user=self.user)
        sample_recipe(user=self.user)
        res = self.client.get(RECIPES_URL)
        recipes = Recipe.objects.all().order_by('-id')
        serializer = RecipeSerializer(recipes, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_recipes_limited_to_user(self):
        """Test that recipe returned are for the authenticated user"""
        user2 = get_user_model().objects.create_user(
            'do1@gmail.com', 'testpass')
        sample_recipe(user=user2)
        recipe = sample_recipe(user=self.user)
        res = self.client.get(RECIPES_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['title'], recipe.title)

    # def test_create_recipe_successful(self):
    #     """Test creating a new recipe"""
    #     payload = {'title': 'Test tag', 'time_minutes': 5, 'price': 10.00}
    #     self.client.post(RECIPES_URL, payload)
    #     exists = Recipe.objects.filter(
    #         user=self.user
    #     ).exists()
    #     self.assertTrue(exists)
    #
    # def test_create_recipe_invalid(self):
    #     """Test creating a new recipe with invalid payload"""
    #     payload = {'title': ''}
    #     res = self.client.post(RECIPES_URL, payload)
    #     self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
