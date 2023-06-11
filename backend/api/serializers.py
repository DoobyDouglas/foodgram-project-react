from rest_framework import serializers
from users.models import User
from recipe.models import Tag, Recipe, Ingredient, Amount
from .exceptions import UsernameValueException
from drf_extra_fields.fields import Base64ImageField
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError
from PIL import Image, UnidentifiedImageError
import re


class RegistrationSerializer(serializers.ModelSerializer):

    def validate_username(self, value):
        match = re.match(r'(?P<username>[\w.@+-]+)', value)
        if not match:
            raise UsernameValueException()
        return value

    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    class Meta:

        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'password',
        )
        extra_kwargs = {'password': {'write_only': True}}


class UserSerializer(serializers.ModelSerializer):

    is_subscribed = serializers.SerializerMethodField()

    def get_is_subscribed(self, author):
        user = self.context['request'].user
        if user.is_anonymous or user == author:
            return False
        return user.follower.filter(author=author).exists()

    class Meta:

        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
        )
        read_only_fields = ('is_subscribed',)


class UserRecipeSerializer(serializers.ModelSerializer):

    is_subscribed = serializers.SerializerMethodField()

    def get_is_subscribed(self, author):
        user = self.context['request'].user
        if user.is_anonymous or user == author:
            return False
        return user.follower.filter(author=author).exists()

    class Meta:

        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
        )
        read_only_fields = ('is_subscribed',)


class SubscribeRecipeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'image',
            'cooking_time',
        )


class SubscribeSerializer(serializers.ModelSerializer):

    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    def get_recipes(self, user):
        recipes_limit = self.context.get('recipes_limit')
        queryset = Recipe.objects.filter(author=user)
        if recipes_limit:
            queryset = queryset[:int(recipes_limit)]
        serializer = SubscribeRecipeSerializer(
            queryset,
            many=True,
            context=self.context,
        )
        return serializer.data

    def get_recipes_count(self, user):
        return user.recipes.count()

    class Meta:

        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'recipes',
            'recipes_count',
        )
        read_only_fields = ('__all__',)


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = '__all__'


class IngredientRecipeSerializer(serializers.ModelSerializer):

    amount = serializers.SerializerMethodField()

    def get_amount(self, ingredient):
        amount = ingredient.amount.values('amount')
        return amount[0]['amount']

    class Meta:

        model = Ingredient
        fields = (
            'id',
            'name',
            'measurement_unit',
            'amount',
        )


class RecipeSerializer(serializers.ModelSerializer):

    tags = TagSerializer(many=True, read_only=True)
    author = UserSerializer(read_only=True)
    ingredients = IngredientRecipeSerializer(many=True, read_only=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    def get_is_favorited(self, recipe):
        user = self.context['request'].user
        if user.is_anonymous:
            return False
        return user.user_favorites.filter(recipe=recipe).exists()

    def get_is_in_shopping_cart(self, recipe):
        user = self.context['request'].user
        if user.is_anonymous:
            return False
        return user.shopping_cart.filter(recipe=recipe).exists()

    class Meta:

        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time',
        )


class IngredientAmountSerializer(serializers.ModelSerializer):

    id = serializers.IntegerField()

    class Meta:

        model = Amount
        fields = (
            'id',
            'amount',
        )


class CreateRecipeSerializer(serializers.ModelSerializer):

    ingredients = IngredientAmountSerializer(many=True)
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True
    )
    image = Base64ImageField()

    def create(self, validated_data):
        request = self.context.get('request')
        tags = validated_data.pop('tags')
        recipe_ingredients = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(**validated_data)
        recipe.author = request.user
        recipe.tags.set(tags)
        for ingredient in recipe_ingredients:
            amount = ingredient['amount']
            ingredient = get_object_or_404(Ingredient, pk=ingredient['id'])
            Amount.objects.create(
                recipe=recipe,
                ingredients=ingredient,
                amount=amount,
            )
        recipe.save()
        return recipe

    def update(self, instance, validated_data):
        tags = validated_data.pop('tags')
        recipe_ingredients = validated_data.pop('ingredients')
        recipe = instance
        recipe.tags.clear()
        recipe.tags.add(*tags)
        Amount.objects.filter(recipe=recipe).delete()
        for key, value in validated_data.items():
            setattr(recipe, key, value)
        for ingredient in recipe_ingredients:
            amount = ingredient['amount']
            ingredient = get_object_or_404(Ingredient, pk=ingredient['id'])
            Amount.objects.create(
                recipe=recipe,
                ingredients=ingredient,
                amount=amount,
            )
        recipe.save()
        return recipe

    # def validate_image(self, value):
    #     try:
    #         image = Image.open(value)
    #         image.verify()
    #     except Exception as e:
    #         raise ValidationError('Файл не является изображением.') from e
    #     return value

    # def validate(self, attrs):
    #     attrs = super().validate(attrs)
    #     image = attrs.get('image')
    #     if image:
    #         attrs['image'] = self.validate_image(image)
    #     return attrs

    class Meta:

        model = Recipe
        fields = (
            'ingredients',
            'tags',
            'image',
            'name',
            'text',
            'cooking_time',
        )


class IngredienteSerializer(serializers.ModelSerializer):

    class Meta:

        model = Ingredient
        fields = '__all__'


class RecipeDetailSerializer(serializers.ModelSerializer):

    tags = TagSerializer(many=True, read_only=True)
    author = UserRecipeSerializer(read_only=True)
    ingredients = IngredientRecipeSerializer(many=True)
    image = serializers.SerializerMethodField()
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    def get_image(self, recipe):
        request = self.context.get('request')
        if request:
            absolute_image_url = request.build_absolute_uri(recipe.image.url)
            return absolute_image_url
        return None

    def get_is_favorited(self, recipe):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return user.user_favorites.filter(recipe=recipe).exists()

    def get_is_in_shopping_cart(self, recipe):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return user.shopping_cart.filter(recipe=recipe).exists()

    class Meta:

        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time',
        )
