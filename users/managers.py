from django.db import models
from django.contrib.auth.models import BaseUserManager

import random

class CustomUserManager(BaseUserManager):

    def create_user(self, email, name, surname, password=None, avatar=None, **extra_fields):
        if not email:
            raise ValueError('Пользователь должен иметь email')
        if not name:
            raise ValueError('Пользователь должен иметь Имя')
        if not surname:
            raise ValueError('Пользователь должен иметь Фамилию')
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            name=name,
            surname=surname,
            **extra_fields
        )

        # Генерируем аватарку, если не передана
        if avatar is None:
            user.avatar = self._generate_avatar(name)

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, name, surname, password=None, avatar=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, name, surname, password, **extra_fields)

    def _generate_avatar(self, name):
        """
        Генерирует аватарку с первой буквой имени на однотонном фоне.
        Фон выбирается из палитры пастельных цветов для хорошей читаемости.
        """
        from PIL import Image, ImageDraw, ImageFont
        import io
        import base64

        # Палитра пастельных цветов (RGB)
        colors = [
            (255, 182, 193),  # Светло-розовый
            (173, 216, 230),  # Светло-голубой
            (144, 238, 144),  # Светло-зелёный
            (250, 250, 210),  # Светло-жёлтый
            (221, 160, 221),  # Сиреневый
            (240, 230, 140),  # Палевый
            (230, 230, 250),  # Лавандовый
        ]

        bg_color = random.choice(colors)
        text_color = (50, 50, 50)  # Тёмно-серый для контраста

        # Создаём изображение 128x128
        image = Image.new('RGB', (128, 128), bg_color)
        draw = ImageDraw.Draw(image)

        # Получаем первую букву имени
        first_letter = name[0].upper()

        # Подбираем шрифт (пытаемся использовать системный, иначе дефолтный)
        try:
            font = ImageFont.truetype('arial.ttf', 80)
        except:
            font = ImageFont.load_default()

        # Центрируем текст
        bbox = draw.textbbox((0, 0), first_letter, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        x = (128 - text_width) // 2
        y = (128 - text_height) // 2 - 10  # Немного поднимаем для визуального баланса

        draw.text((x, y), first_letter, fill=text_color, font=font)

        # Сохраняем в байтовый поток
        buffer = io.BytesIO()
        image.save(buffer, format='PNG')
        avatar_data = buffer.getvalue()

        # Кодируем в base64 для хранения в ImageField
        avatar_base64 = base64.b64encode(avatar_data).decode('utf-8')

        return f'data:image/png;base64,{avatar_base64}'