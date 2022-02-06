from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Tag
from ..serializers import TagSerializer

TAGS_URL = reverse('recipe:tag-list')


class PublicTagApiTest(TestCase):
    """ Test the publicly available tags API """

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """ Test that login for receiving tags """
        res = self.client.get(TAGS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTagsApiTest(TestCase):
    """ Test the authorized user tags api """

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            'test@gmail.com',
            'password',
        )
        # Init Api CLient
        self.client = APIClient()
        # Authenticate created user
        self.client.force_authenticate(self.user)

    def test_retrieve_tags(self):
        """ Test retreiving tags """
        Tag.objects.create(user=self.user, name='Vegan')
        Tag.objects.create(user=self.user, name='Dessert')

        res = self.client.get(TAGS_URL)

        tags = Tag.objects.all().order_by('-name')
        serializer = TagSerializer(tags, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_tags_limited_to_user(self):
        """ Test that tags returned are for the authenticated user """
        user2 = get_user_model().objects.create_user(
            'other@gmail.com',
            'testpass'
        )

        Tag.objects.create(user=user2, name='Frutty')
        tag = Tag.objects.create(user=self.user, name='Food')

        # Create request
        res = self.client.get(TAGS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], tag.name)

    def test_create_tag_successfull(self):
        """ Test creating a new Tag """
        payload = {'name': 'test tag'}
        self.client.post(TAGS_URL, payload)

        exist = Tag.objects.filter(
            user=self.user, name=payload['name']
        ).exists()

        self.assertTrue(exist)

    def test_create_tag_invalid(self):
        payload = {'name': ''}
        res = self.client.post(TAGS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
