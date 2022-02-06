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

    def test_retrieve_ingredients_list(self):
        """ Test retrieving a list of ingredients """
        Ingredient.objects.create(user=self.user, name='Cucu')
        Ingredient.objects.create(user=self.user, name='AHAHA')

        res = self.client.get(INGREDIENTS_URL)

        ingredientsList = Ingredient.objects.all().order_by('-name')
        serializer = IngredientSerializer(ingredientsList, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_ingredients_lomited_to_user(self):
        """ Test that ingredients for the authenticated user are returned """
        user = get_user_model().objects.create(
            'test@gmail.com',
            'testpass'
        )
        Ingredient.objects.create(user=user, name='Vinegar')
        ingredient = Ingredient.objects.create(user=self.user, name='Sugar')

        res = self.client.get(INGREDIENTS_URL)

        self.assertEqual(rest.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], ingredient.name)
