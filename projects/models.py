from django.db import models


class Project(models.Model):
    CHOICES = [
        ("open", "Открыт"),
        ("closed", "Закрыт")
    ]

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
        'users.CustomUser',
        on_delete=models.CASCADE,
        related_name='owned_projects',
        verbose_name='Автор проекта'
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания проекта'
    )

    github_url = models.URLField(
        unique=True,
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
        'users.CustomUser',
        blank=True,
        related_name='participated_projects',
        verbose_name='Участники проекта'
    )

    skills = models.ManyToManyField(
        'Skill',
        blank=True,
        related_name='projects',
        verbose_name='Навыки, необходимые проекту'
    )

    class Meta:
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'
        ordering = ['-created_at']

    def __str__(self):
        return self.name


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
