from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    email = models.EmailField(
        max_length=254,
        unique=True,
        verbose_name='Почта',
    )
    username = models.CharField(
        max_length=150,
        unique=True,
        verbose_name='Имя пользователя',
    )
    first_name = models.CharField(
        max_length=150,
        blank=False,
        verbose_name='Имя',
    )
    last_name = models.CharField(
        max_length=150,
        blank=False,
        verbose_name='Фамилия',
    )
    password = models.CharField(
        max_length=150,
        verbose_name='Пароль',
    )
    is_superuser = models.BooleanField(
        default=False,
        help_text=('Администратор'),
    )

    def __str__(self):
        return self.username

    class Meta:

        ordering = ('username',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Subscription(models.Model):

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Автор'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик'
    )

    def __str__(self):
        return f'{self.user} подписан(а) на {self.author}'

    class Meta:

        ordering = ('author',)
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'user'],
                name='unique_subscription',
            ),
        ]
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
