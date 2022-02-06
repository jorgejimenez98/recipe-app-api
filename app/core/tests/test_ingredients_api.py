from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from ..models import Ingredient
from ..serializers import IngredientSerializer

INGREDIENTS_URL = reverse('recipe:ingredient-list')


class PublicIngredientsApiTest(TestCase):
    """ Test the public availlable ingredients API """

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """ Test that login is required to access the endpoint """
        res = self.client.get(INGREDIENTS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateIngredientsApiTest(TestCase):
    """ Test Ingredients can be retrieved by authorized user """

    def setUp(self):
        self.client = APIClient()
        # Create User
        self.user = get_user_model().objects.create_user(
            'test@gmail.com',
            'testpass'
        )
        # Authenticate User
        self.client.force_authenticate(self.user)
