from django.db import models
from users.models import User
from django.core.validators import MinValueValidator, RegexValidator


class Tag(models.Model):

    name = models.CharField(
        max_length=25,
        unique=True,
        verbose_name='Имя тэга',
    )
    color = models.CharField(
        max_length=7,
        unique=True,
        verbose_name='Цвет тэга',
    )
    slug = models.CharField(
        max_length=15,
        unique=True,
        verbose_name='Слаг тэга'
    )

    def __str__(self):
        return self.name

    class Meta:

        ordering = ('name',)
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'


class Ingredient(models.Model):

    name = models.CharField(
        max_length=50,
        verbose_name='Название',
    )
    measurement_unit = models.CharField(
        verbose_name='Единицы измерения',
        max_length=25,
    )

    def __str__(self):
        return self.name

    class Meta:

        ordering = ('name', )
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'


class Recipe(models.Model):

    author = models.ForeignKey(
        User,
        null=True,
        on_delete=models.SET_NULL,
        related_name='recipes',
        verbose_name='Автор',
    )
    name = models.CharField(
        verbose_name='Рецепт',
        max_length=200,
    )
    image = models.ImageField(
        verbose_name='Изображение',
        upload_to='recipes/images/',
    )
    text = models.TextField(
        verbose_name='Описание',
        max_length=254,
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='Amount',
        related_name='recipes',
        verbose_name='Ингредиенты блюда',
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='recipes',
        verbose_name='Тэги блюда',
    )
    cooking_time = models.PositiveSmallIntegerField(
        default=1,
        validators=[
            RegexValidator(
                r'^\d+$', 'Значение должно быть целым числом.', 'invalid'
            ),
            MinValueValidator(1, message='0 минут не может быть'),
        ],
        verbose_name='Время приготовления в минутах',
    )

    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации рецепта',
    )

    def __str__(self):
        return self.name

    class Meta:

        ordering = ('-pub_date', )
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'


class Amount(models.Model):

    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Связанные рецепты',
        related_name='amount',
    )
    ingredients = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='amount',
        verbose_name='Ингредиенты блюда',
    )
    amount = models.PositiveSmallIntegerField(
        default=1,
        validators=[MinValueValidator(1, message='0 штук не может быть'), ],
        verbose_name='Количество',
    )

    def __str__(self):
        return (
            f'{self.ingredients}: {self.amount} '
            f'{self.ingredients.measurement_unit}'
        )

    class Meta:

        ordering = ('recipe', )
        verbose_name = 'Ингредиенты в блюде'
        verbose_name_plural = 'Ингредиенты в блюдах'


class Favorite(models.Model):

    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Избранный рецепт',
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user_favorites',
        verbose_name='Пользователь',
    )

    def __str__(self):
        return f'{self.user} любит {self.recipe}'

    class Meta:

        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'user'],
                name='unique_favorite',
            ),
        ]
        verbose_name = 'Избранный рецепт'
        verbose_name_plural = 'Избранные рецепты'


class ShoppingСart(models.Model):

    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='in_shopping_carts',
        verbose_name='Рецепт в списке покупок',
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shopping_cart',
        verbose_name='Владелец списка покупок',
    )

    def __str__(self) -> str:
        return f'{self.recipe} для {self.user}'

    class Meta:

        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'user'],
                name='unique_shoppingcart',
            ),
        ]
        verbose_name = 'Рецепт в списке покупок'
        verbose_name_plural = 'Рецепты в списке покупок'
