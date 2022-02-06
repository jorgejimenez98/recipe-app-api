from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Ingredient
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
        user2 = get_user_model().objects.create_user(
            'other@gmail.com',
            'testpass3'
        )
        Ingredient.objects.create(user=user2, name='Vinegar')
        ingredient = Ingredient.objects.create(user=self.user, name='Sugar')

        res = self.client.get(INGREDIENTS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], ingredient.name)

    def test_create_ingredient_successfull(self):
        """ Test to create ingredient successfully """
        payload = {'name': 'nameSample'}
        self.client.post(INGREDIENTS_URL, payload)

        exists = Ingredients.object.filter(
            user=self.user,
            name=payload['name']
        ).exists()

        self.assertTrue(exists)

    def test_create_ingredient_fail(self):
        """ Test to create ingredient fail """
        payload = {'name': ''}
        res = self.client.post(INGREDIENTS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
