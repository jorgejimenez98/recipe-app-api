from django.test import TestCase
from django.contrib.auth import get_user_model
from ..models import Ingredient


class ModelTests(TestCase):

    def test_create_user_with_email_successfully(self):
        """ Test creating a new user with an email is successfully """
        email = "test@gmail.com"
        password = "testpass123"
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalize(self):
        """ Test the email for a new user is normalized """
        email = "test@GMAIL.com"
        user = get_user_model().objects.create_user(email, 'test123')

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """ Test creating user with no email raises error """
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(
                None,
                'test123'
            )

    def test_create_new_superuser(self):
        """ Test creating a new superuser """
        user = get_user_model().objects.create_superuser(
            'test@gmail.com',
            'test123'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_ingredient_str(self):
        """ Test the ingredient string representation """

        # Create User
        email = "test@gmail.com"
        password = "testpass123"
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        ingredient = Ingredient.objects.create(
            user=user,
            name='Cucumber'
        )

        self.assertEqual(str(ingredient), ingredient.name)
