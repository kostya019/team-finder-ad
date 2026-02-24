from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.

#
# !!! Добавить  UserManager
#
# Добавить в Project внешний ключ на Skill
#
# Добавить необходимые методы к моделям
#

User = get_user_model()

CHOICES = [
    ("open", "Open"),
    ("closed", "Closed")
]

class Project(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name="Название проекта"
    )

    description = models.TextField(
        blank=True,
        null=True,
        verbose_name='Описание проекта'
    )

    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор проекта'
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания проекта'
    )

    github_url = models.URLField(
        blank=True,
        null=True,
        verbose_name='Ссылка на Github'
    )

    status = models.CharField(
        max_length=6,
        choices=CHOICES,
        verbose_name='Статус проекта'
    )

    participants = models.ManyToManyField(
        User,
        blank=True,
        related_name='participants',
        verbose_name='Участники проекта'
    )

    class Meta:
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'

    def __str__(self):
        return self.name

class Users(models.Model):
    email = models.EmailField(
        unique=True,
        verbose_name='Адрес электронной почты'
    )

    name = models.CharField(
        max_length=124,
        verbose_name='Имя пользователя'
    )

    surname = models.CharField(
        max_length=124,
        verbose_name='Фамилия пользователя'
    )

    avatar = models.ImageField(
        verbose_name='Аватарка пользователя'
    )

    phone = models.CharField(
        max_length=12,
        verbose_name='Номер телефона'
    )

    github_url = models.URLField(
        blank=True,
        null=True,
        verbose_name='Ссылка на Github'
    )

    about = models.TextField(
        max_length=256,
        blank=True,
        null=True,
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

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f'{self.name} {self.surname}'

class Skill(models.Model):
    name = models.CharField(
        max_length=124,
        verbose_name='Название навыка'
    )

    class Meta:
        verbose_name = 'Навык'
        verbose_name_plural = 'Навыки'

    def __str__(self):
        return self.name