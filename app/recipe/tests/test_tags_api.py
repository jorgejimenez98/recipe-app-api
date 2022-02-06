from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Tag
from core.serializers import TagSerializer

TAGS_URL = reverse('recipe:tag-list')


class PublicTagApiTest(TestCase):
    """ Test the publicly available tags API """

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """ Test that login for receiving tags """
        res = self.client.get(TAGS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAITOHRIZED)
