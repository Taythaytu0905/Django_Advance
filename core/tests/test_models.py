from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.test import TestCase

from core import models

User = get_user_model()


def sample_user(email='do@gmail.com', password='testcase'):
    return get_user_model().objects.create_user(email, password)


class ModelTest(TestCase):

    def test_create_user_with_email_successful(self):
        email = "ntdo.13cdt1@gmail.com"
        password = "doxike123"
        user = User.objects.create_user(email=email, password=password)
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_email_format(self):
        email = "ntdo.13cdt1@GMAIL.COM"
        user = User.objects.create_user(email=email, password='doxike123')
        self.assertEqual(user.email, email.lower())

    def test_validation_email(self):
        with self.assertRaises(ValueError):
            User.objects.create_user(None, 'doxike123')

    def test_create_super_user(self):
        email = 'ntdo.13cdt1@gmail.com'
        password = 'doxike1234'
        user = User.objects.create_superuser(
            email=email, password=password, is_superuser=True, is_staff=True
        )
        self.assertEqual(user.is_superuser, True)

    def test_tag_str(self):
        tag = models.Tag.objects.create(
            user=sample_user(),
            name='Vegan'
        )
        self.assertEqual(str(tag), tag.name)

    def test_ingredient_str(self):
        """Test the ingredient string representation"""
        ingredient = models.Ingredient.objects.create(
            user=sample_user(),
            name='Cucumber'
        )
        self.assertEqual(str(ingredient), ingredient.name)

    def test_recipe_str(self):
        """Test the recipe string representation"""
        recipe = models.Recipe.objects.create(
            user=sample_user(),
            title='Chicken rice',
            time_minutes=5,
            price=5.00
        )
        self.assertEqual(str(recipe), recipe.title)

    @patch("uuid.uuid4")
    def test_recipe_file_name_uuid(self, mock_uuid):
        """Test that image is saved in the correct location"""
        uuid = "test-uuid"
        mock_uuid.return_value = uuid
        file_path = models.recipe_image_file_path(None, 'image.jpg')
        exp_path = f'uploads/recipe/{uuid}.jpg'
        self.assertEqual(file_path, exp_path)
