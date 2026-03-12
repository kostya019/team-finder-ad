import io
import random
import logging
import os
from PIL import Image, ImageDraw, ImageFont
from django.core.files import File
from django.core.files.storage import default_storage

logger = logging.getLogger(__name__)


def get_font(size=80):
    # Список возможных путей к шрифтам в контейнере
    font_paths = [
        '/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf',
        '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',
        '/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf',
        'arial.ttf',  # на случай, если есть на хосте (не в Docker)
    ]
    for path in font_paths:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except OSError:
                continue
    # Запасной вариант – дефолтный шрифт (будет мелким)
    return ImageFont.load_default()


def generate_avatar_image(name: str) -> Image.Image:
    """Генерирует изображение аватара с первой буквой имени."""
    colors = [
        (255, 182, 193), (173, 216, 230), (144, 238, 144), (250, 250, 210),
        (221, 160, 221), (240, 230, 140), (230, 230, 250), (254, 214, 188),
        (239, 169, 74), (255, 117, 20), (93, 155, 155), (127, 181, 181),
        (222, 247, 254), (255, 254, 224), (250, 248, 246), (29, 236, 248),
        (255, 209, 220), (161, 133, 148)
    ]
    bg_color = random.choice(colors)
    text_color = (50, 50, 50)

    image = Image.new('RGB', (128, 128), bg_color)
    draw = ImageDraw.Draw(image)

    first_letter = name[0].upper() if name else '?'

    font = get_font(80)

    bbox = draw.textbbox((0, 0), first_letter, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    x = (128 - text_width) // 2
    y = (128 - text_height) // 2 - 10

    draw.text((x, y), first_letter, fill=text_color, font=font)
    return image


def save_avatar_image(image: Image.Image, name: str, surname: str) -> str:
    """Сохраняет изображение в хранилище и возвращает путь."""
    image_buffer = io.BytesIO()
    image.save(image_buffer, format='PNG')
    image_buffer.seek(0)

    # Генерируем уникальное имя файла
    avatar_filename = f'avatar_{name}_{surname}_{random.randint(1000, 9999)}.png'
    # Сохраняем через default_storage
    avatar_path = default_storage.save(f'avatars/{avatar_filename}', File(image_buffer))
    return avatar_path
