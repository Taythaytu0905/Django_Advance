from django.contrib.auth import get_user_model
from django.test import TestCase

User = get_user_model()


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
