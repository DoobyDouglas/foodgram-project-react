from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from users.models import User
from .serializers import UserSerializer
from .paginators import Pagination
from djoser.views import UserViewSet as DUserViewSet
from .permissions import ObjAuthorOrReadOnly


class UserViewSet(DUserViewSet, viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = Pagination
    http_method_names = ['get', 'post']
