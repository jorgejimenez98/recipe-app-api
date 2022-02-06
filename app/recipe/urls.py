from django.urls import path
from django.conf.urls import include
from rest_framework.routers import DefaultRouter

from .views import TagsViewSet

router = DefaultRouter()
router.register('tags', TagsViewSet)

app_name = 'recipe' # this is for test reconize reverse urls

urlpatterns = [
    path('', include(router.urls))
]
