import re
from urllib.parse import urlparse

from django.conf.settings import ALLOWED_GITHUB_DOMAINS
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_github_repo_url(value):
    """
    Валидатор для проверки ссылки на конкретный репозиторий GitHub.
    Проверяет формат: github.com/<username>/<repository>
    """
    parsed_url = urlparse(value)
    domain = parsed_url.netloc.lower()

    # Проверка домена
    if domain not in ALLOWED_GITHUB_DOMAINS:
        raise ValidationError(
            _('Ссылка должна вести на github.com'),
            code='invalid_domain'
        )

    # Проверка пути — должен соответствовать формату /<username>/<repo>
    path = parsed_url.path.strip('/')
    pattern = r'^[a-zA-Z0-9_-]+/[a-zA-Z0-9_-]+$'

    if not re.match(pattern, path):
        raise ValidationError(
            _('Некорректный формат URL репозитория. Ожидаемый формат: github.com/username/repository'),
            code='invalid_repo_format'
        )

    return value
