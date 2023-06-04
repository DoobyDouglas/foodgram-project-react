from rest_framework import viewsets, status
from users.models import User, Subscription
from .serializers import (
    UserSerializer,
    TagSerializer,
    RecipeSerializer,
    SubscribeSerializer,
    IngredienteSerializer,
    CreateRecipeSerializer,
    RecipeDetailSerializer,
)
from .paginators import Pagination
from djoser.views import UserViewSet as DjoserUVS
from recipe.models import Tag, Recipe, Favorite, Ingredient, ShoppingСart
from .permissions import ObjAuthorOrReadOnly
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from django.http import HttpResponse


class UserViewSet(DjoserUVS, viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = Pagination
    permission_classes = (IsAuthenticated, ObjAuthorOrReadOnly)
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
        recipes_limit = self.request.query_params.get('recipes_limit')
        serializer = SubscribeSerializer(
            queryset,
            many=True,
            context={'request': request, 'recipes_limit': recipes_limit},
        )
        return self.get_paginated_response(serializer.data)

    subscribe_args = {
        'methods': ('post', 'delete',),
        'detail': True,
        'permission_classes': (IsAuthenticated,),
    }

    @action(**subscribe_args)
    def subscribe(self, request, id):
        user = request.user
        author = get_object_or_404(User, pk=id)
        subscription = Subscription.objects.filter(
            author=author,
            user=user
        )
        if request.method == 'POST':
            if subscription.exists():
                return Response(status=status.HTTP_400_BAD_REQUEST)
            Subscription.objects.create(author=author, user=user)
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
    filter_backends = (DjangoFilterBackend,)
    http_method_names = ('get', 'post', 'patch', 'delete',)

    def create(self, request, *args, **kwargs):
        serializer = CreateRecipeSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            self.perform_create(serializer)
            recipe = serializer.instance
            recipe.author = request.user
            recipe.save()
            serializer = RecipeDetailSerializer(
                recipe,
                context={'request': request},
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk, partial):
        instance = self.get_object()
        serializer = RecipeSerializer(
            instance,
            data=request.data,
            partial=partial,
            context={'request': request},
        )
        if serializer.is_valid(raise_exception=True):
            self.perform_update(serializer)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        user = self.request.user
        queryset = self.queryset
        is_favorited = self.request.query_params.get('is_favorited')
        if is_favorited == '1':
            queryset = queryset.filter(favorites__user=user)
        elif is_favorited == '0':
            queryset = queryset.exclude(favorites__user=user)
        in_cart = self.request.query_params.get('is_in_shopping_cart')
        if in_cart == '1':
            queryset = queryset.filter(in_shopping_carts__user=user)
        elif in_cart == '0':
            queryset = queryset.exclude(in_shopping_carts__user=user)
        author = self.request.query_params.get('author')
        if author:
            queryset = queryset.filter(author=author)
        tags = self.request.query_params.getlist('tags')
        if tags:
            queryset = queryset.filter(tags__slug__in=tags)
        return queryset

    favorite_args = {
        'methods': ('post', 'delete',),
        'detail': True,
        'permission_classes': (IsAuthenticated,)
    }

    @action(**favorite_args)
    def favorite(self, request, pk):
        user = request.user
        recipe = get_object_or_404(Recipe, pk=pk)
        favorite = Favorite.objects.filter(recipe=recipe, user=user)
        if request.method == 'POST':
            if favorite.exists():
                return Response(status=status.HTTP_400_BAD_REQUEST)
            Favorite.objects.create(recipe=recipe, user=user)
            return Response(status=status.HTTP_201_CREATED)
        if request.method == 'DELETE':
            if favorite.exists():
                favorite.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    shopping_cart_args = {
        'methods': ('post', 'delete',),
        'detail': True,
        'permission_classes': (IsAuthenticated,)
    }

    @action(**shopping_cart_args)
    def shopping_cart(self, request, pk):
        user = request.user
        recipe = get_object_or_404(Recipe, pk=pk)
        in_cart = ShoppingСart.objects.filter(recipe=recipe, user=user)
        if request.method == 'POST':
            if in_cart.exists():
                return Response(status=status.HTTP_400_BAD_REQUEST)
            ShoppingСart.objects.create(recipe=recipe, user=user)
            return Response(status=status.HTTP_201_CREATED)
        if request.method == 'DELETE':
            if in_cart.exists():
                in_cart.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    download_args = {
        'methods': ('get',),
        'detail': False,
        'permission_classes': (IsAuthenticated,)
    }

    @action(**download_args)
    def download_shopping_cart(self, request):
        user = request.user
        if user.shopping_cart.exists():
            filename = 'shopping_list.txt'
            ingredients_dict = {}
            file = []
            head = 'Ваш список покупок:\n'
            file.append(head)
            for cart in user.shopping_cart.all():
                for i in cart.recipe.amount.all():
                    name = i.ingredients.name
                    amount = i.amount
                    unit = i.ingredients.measurement_unit
                    if name in ingredients_dict:
                        ingredients_dict[name][0] += amount
                        continue
                    ingredients_dict[name] = [amount, unit]
            for key, value in ingredients_dict.items():
                print(value)
                file.append(f'{key} {value[0]} {value[1]}\n')
            response = HttpResponse(
                file,
                content_type='text/plain'
            )
            response['Content-Disposition'] = (
                f'attachment; filename="{filename}"'
            )
            return response
        return Response(status=status.HTTP_400_BAD_REQUEST)


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredienteSerializer
    http_method_names = ('get',)
