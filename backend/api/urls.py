from django.urls import include, path
from rest_framework import routers
from .views import UserViewSet, TagViewSet, RecipeViewSet

app_name = 'api'

router = routers.DefaultRouter()
router.register('users', UserViewSet, 'users')
router.register('tags', TagViewSet, 'tags')
router.register('recipes', RecipeViewSet, 'recipes')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('djoser.urls.authtoken')),
]
