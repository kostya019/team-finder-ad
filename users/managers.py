from django.contrib.auth.models import BaseUserManager
from .avatar_utils import generate_avatar_image, save_avatar_image
import logging

logger = logging.getLogger(__name__)


class CustomUserManager(BaseUserManager):

    def create_user(self, email, name, surname, avatar=None, password=None, **extra_fields):
        if not email:
            raise ValueError('Пользователь должен иметь email')
        if not name:
            raise ValueError('Пользователь должен иметь Имя')
        if not surname:
            raise ValueError('Пользователь должен иметь Фамилию')
        email = self.normalize_email(email)
        if avatar is None:
            try:
                image = generate_avatar_image(name)
                avatar = save_avatar_image(image, name, surname)
            except Exception as e:
                logger.error(f"Ошибка генерации аватара для {name}: {e}")
                avatar = None

        user = self.model(
            email=email,
            name=name,
            surname=surname,
            avatar=avatar,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, surname, avatar=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, name, surname, avatar, password, **extra_fields)
