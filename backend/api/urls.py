from django.urls import include, path
from rest_framework import routers
from .views import UserViewSet

app_name = 'api'
router = routers.DefaultRouter()
router.register('users', UserViewSet, basename='users')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('djoser.urls.authtoken')),
]
