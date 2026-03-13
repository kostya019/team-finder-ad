import io
import logging
import os
import random

from PIL import Image, ImageDraw, ImageFont
from django.core.files import File
from django.core.files.storage import default_storage

from core.constants import (
    AVATAR_BACKGROUND_COLORS,
    AVATAR_FONT_SIZE,
    AVATAR_RANDOM_RANGE,
    AVATAR_TEXT_COLOR,
)

logger = logging.getLogger(__name__)


def get_font(size=AVATAR_FONT_SIZE):
    font_paths = [
        '/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf',
        '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',
        '/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf',
        'arial.ttf',
    ]
    for path in font_paths:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except OSError:
                continue
    return ImageFont.load_default()


def generate_avatar_image(name: str) -> Image.Image:
    """Генерирует изображение аватара с первой буквой имени."""
    bg_color = random.choice(AVATAR_BACKGROUND_COLORS)

    image = Image.new('RGB', (128, 128), bg_color)
    draw = ImageDraw.Draw(image)

    first_letter = name[0].upper() if name else '?'
    font = get_font()
    bbox = draw.textbbox((0, 0), first_letter, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    x = (128 - text_width) // 2
    y = (128 - text_height) // 2 - 10

    draw.text((x, y), first_letter, fill=AVATAR_TEXT_COLOR, font=font)
    return image


def save_avatar_image(image: Image.Image, name: str, surname: str) -> str:
    """Сохраняет изображение в хранилище и возвращает путь."""
    image_buffer = io.BytesIO()
    image.save(image_buffer, format='PNG')
    image_buffer.seek(0)

    avatar_filename = f'avatar_{name}_{surname}_{random.randint(*AVATAR_RANDOM_RANGE)}.png'
    avatar_path = default_storage.save(f'avatars/{avatar_filename}', File(image_buffer))
    return avatar_path
