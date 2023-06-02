from rest_framework import viewsets, status
from users.models import User, Subscription
from .serializers import (
    UserSerializer,
    TagSerializer,
    RecipeSerializer,
    SubscribeSerializer,
    IngredienteSerializer,
)
from .paginators import Pagination
from djoser.views import UserViewSet as DjoserUVS
from recipe.models import Tag, Recipe, Favorite, Ingredient
from .permissions import ObjAuthorOrReadOnly
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404


class UserViewSet(DjoserUVS, viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = Pagination
    permission_classes = (ObjAuthorOrReadOnly,)
    http_method_names = ('get', 'post', 'delete',)

    subscriptions_args = {
        'methods': ('get',),
        'detail': False,
        'permission_classes': (IsAuthenticated,),
    }

    @action(**subscriptions_args)
    def subscriptions(self, request):
        queryset = self.paginate_queryset(
            User.objects.filter(following__user=request.user)
        )
        serializer = SubscribeSerializer(queryset, many=True)
        return self.get_paginated_response(serializer.data)

    subscribe_args = {
        'methods': ('post', 'delete',),
        'detail': True,
        'permission_classes': (IsAuthenticated,),
    }

    @action(**subscribe_args)
    def subscribe(self, request, id):
        author = get_object_or_404(User, pk=id)
        subscription = Subscription.objects.filter(
            author=author,
            user=request.user
        )
        if request.method == 'POST':
            if subscription.exists():
                return Response(status=status.HTTP_400_BAD_REQUEST)
            Subscription.objects.create(author=author, user=request.user)
            return Response(status=status.HTTP_201_CREATED)
        if request.method == 'DELETE':
            if subscription.exists():
                subscription.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_401_UNAUTHORIZED)


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    http_method_names = ('get',)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    pagination_class = Pagination
    permission_classes = (ObjAuthorOrReadOnly,)
    http_method_names = ('get', 'post', 'patch', 'delete',)

    def update(self, request, pk, partial):
        instance = self.get_object()
        serializer = RecipeSerializer(
            instance,
            data=request.data,
            partial=partial,
        )
        if serializer.is_valid(raise_exception=True):
            self.perform_update(serializer)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    favorite_args = {
        'methods': ('post', 'delete',),
        'detail': True,
        'permission_classes': (IsAuthenticated,)
    }

    @action(**favorite_args)
    def favorite(self, request, pk):
        recipe = get_object_or_404(Recipe, pk=pk)
        favorite = Favorite.objects.filter(recipe=recipe, user=request.user)
        if request.method == 'POST':
            if favorite.exists():
                return Response(status=status.HTTP_400_BAD_REQUEST)
            Favorite.objects.create(recipe=recipe, user=request.user)
            return Response(status=status.HTTP_201_CREATED)
        if request.method == 'DELETE':
            if favorite.exists():
                favorite.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_401_UNAUTHORIZED)


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredienteSerializer
    http_method_names = ('get',)
