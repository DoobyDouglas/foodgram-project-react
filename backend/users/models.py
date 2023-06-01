from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    ADMIN = 'admin'
    USER = 'user'
    ROLES = [
        (ADMIN, 'admin'),
        (USER, 'user'),
    ]

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
    role = models.CharField(
        max_length=5,
        choices=ROLES,
        default='user',
        verbose_name='Роль',
    )

    @property
    def is_admin(self):
        return self.role == self.ADMIN

    def __str__(self):
        return self.username

    class Meta:
        ordering = ('username',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
