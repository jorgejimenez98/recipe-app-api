from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from .serializers import Tag, Ingredient, TagSerializer, IngredientSerializer, Recipe, RecipeSerializer


class BaseRecipeAttrViewSet(viewsets.GenericViewSet,
                            mixins.ListModelMixin,
                            mixins.CreateModelMixin):
    """ Base viewset for user owned recipe attributes """
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        """ Return objects for the current auth user only """
        return self.queryset.filter(user=self.request.user).order_by('-name')

    def perform_create(self, serializer):
        """ Create a new Object """
        serializer.save(user=self.request.user)


class TagsViewSet(BaseRecipeAttrViewSet):
    """ Manage tags in the database """
    queryset = Tag.objects.all().order_by('-name')
    serializer_class = TagSerializer


class IngredientViewSet(BaseRecipeAttrViewSet):
    """ Manage Ingredients in the database """
    queryset = Ingredient.objects.all().order_by('-name')
    serializer_class = IngredientSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    """ Manage Recipes in the database """
    queryset = Recipe.objects.all().order_by('-pk')
    serializer_class = RecipeSerializer
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """ Retreive the recipe for the authenticatied user """
        return self.queryset.filter(user=self.request.user)
