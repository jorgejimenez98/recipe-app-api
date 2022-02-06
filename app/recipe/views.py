from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from .serializers import Tag, Ingredient, TagSerializer, IngredientSerializer


class TagsViewSet(viewsets.GenericViewSet,
                  mixins.ListModelMixin,
                  mixins.CreateModelMixin):
    """ Manage tags in the database """
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]
    queryset = Tag.objects.all().order_by('-name')
    serializer_class = TagSerializer

    def get_queryset(self):
        """ Return object for the current auth user only """
        return self.queryset.filter(user=self.request.user).order_by('-name')

    def perform_create(self, serializer):
        """ Create a new Tag """
        serializer.save(user=self.request.user)


class IngredientViewSet(viewsets.GenericViewSet,
                        mixins.ListModelMixin):
    """ Manage Ingredients in the database """
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]
    queryset = Ingredient.objects.all().order_by('-name')
    serializer_class = IngredientSerializer

    def get_queryset(self):
        """ Return object for the current auth user only """
        return self.queryset.filter(user=self.request.user).order_by('-name')
