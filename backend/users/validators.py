import re
from urllib.parse import urlparse

import requests
from django.conf.settings import ALLOWED_GITHUB_DOMAINS
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from core.constants import PHONE_NUMBER_MAX_LENGTH


def validate_no_digits(value):
    value = value.strip()
    if not value:
        raise ValidationError(_('Это поле обязательно для заполнения.'))
    if re.search(r'\d', value):
        raise ValidationError(_('Имя не должно содержать цифр.'))
    return value


def validate_phone_number(value):
    """
    Валидатор для номера телефона.
    Принимает форматы: 8XXXXXXXXX или +7XXXXXXXXX.
    Преобразует в формат +7XXXXXXXXX.
    """
    # Убираем все нецифровые символы, кроме + в начале
    cleaned = re.sub(r'[^\d+]', '', value)

    # Проверяем, начинается ли номер с 8 или +7
    if cleaned.startswith('8'):
        cleaned = '+7' + cleaned[1:]
    elif cleaned.startswith('+7'):
        pass
    else:
        raise ValidationError(
            _('Номер должен начинаться с 8 или +7'),
            code='invalid_format'
        )

    if len(cleaned) != PHONE_NUMBER_MAX_LENGTH:
        raise ValidationError(
            _('Некорректная длина номера'),
            code='invalid_length'
        )

    if not re.match(r'\+7\d{10}', cleaned):
        raise ValidationError(
            _('Номер содержит недопустимые символы'),
            code='invalid_characters'
        )
    return cleaned


def validate_github_url(value):
    """
    Валидатор для проверки ссылки на GitHub.
    Проверяет, что URL относится к github.com.
    Опционально: проверяет доступность ссылки.
    """
    try:
        parsed_url = urlparse(value)

        if parsed_url.netloc not in ALLOWED_GITHUB_DOMAINS:
            raise ValidationError(
                _('Ссылка должна вести на github.com'),
                code='invalid_domain'
            )

    except requests.exceptions.RequestException:
        raise ValidationError(
            _('Ошибка при проверке ссылки'),
            code='request_error'
        )
    except Exception:
        raise ValidationError(
            _('Некорректный URL'),
            code='invalid_url'
        )

    return value
