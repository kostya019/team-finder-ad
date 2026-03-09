from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
import re
from django.core.exceptions import ValidationError

from .validators import validate_no_digits
from .managers import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        unique=True,
        verbose_name='Адрес электронной почты'
    )

    name = models.CharField(
        max_length=124,
        validators=[validate_no_digits],
        verbose_name='Имя пользователя'
    )

    surname = models.CharField(
        max_length=124,
        validators=[validate_no_digits],
        verbose_name='Фамилия пользователя'
    )

    avatar = models.ImageField(
        upload_to='avatars/',
        verbose_name='Аватарка пользователя'
    )

    phone = models.CharField(
        unique=True,
        max_length=12,
        help_text='Форматы: 8XXXXXXXXXX, либо +7XXXXXXXXXX',
        verbose_name='Номер телефона'
    )

    github_url = models.URLField(
        unique=True,
        blank=True,
        null=True,
        help_text='Формат: https://github.com/username',
        verbose_name='Ссылка на Github'
    )

    about = models.TextField(
        max_length=256,
        blank=True,
        null=True,
        help_text='Форматы: 8XXXXXXXXXX, либо +7XXXXXXXXXX. X — цифры.',
        verbose_name='Описание профиля'
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name='Активный пользователь'
    )

    is_staff = models.BooleanField(
        default=False,
        verbose_name='Администратор'
    )

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'surname']

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f'{self.name} {self.surname}'
