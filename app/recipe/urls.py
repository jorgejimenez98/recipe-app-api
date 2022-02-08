from django.urls import path
from django.conf.urls import include
from rest_framework.routers import DefaultRouter

from .views import TagsViewSet, IngredientViewSet, RecipeViewSet

router = DefaultRouter()
router.register('tags', TagsViewSet)
router.register('ingredients', IngredientViewSet)
router.register('recipes', RecipeViewSet)

app_name = 'recipe' # this is for test reconize reverse urls

urlpatterns = [
    path('', include(router.urls))
]
