import re
import requests
from urllib.parse import urlparse
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


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

    if len(cleaned) != 12:
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

        # Проверяем домен
        if parsed_url.netloc not in ['github.com', 'www.github.com']:
            raise ValidationError(
                _('Ссылка должна вести на github.com'),
                code='invalid_domain'
            )

        # Опционально: проверяем доступность ссылки
        # response = requests.head(value, timeout=5, allow_redirects=True)
        # if response.status_code not in [200, 301, 302]:
        #     raise ValidationError(
        #         _('Ссылка недоступна или ведёт на несуществующую страницу'),
        #         code='unreachable_url'
        #     )

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
