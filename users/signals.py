from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser
from .avatar_utils import generate_avatar_image, save_avatar_image
import logging

logger = logging.getLogger(__name__)


@receiver(post_save, sender=CustomUser)
def create_user_avatar(sender, instance, created, **kwargs):
    """Создаёт аватар, если пользователь новый и аватар не задан."""
    if created and not instance.avatar:
        try:
            image = generate_avatar_image(instance.name)
            avatar_path = save_avatar_image(image, instance.name, instance.surname)
            instance.avatar = avatar_path
            instance.save(update_fields=['avatar'])  # сохраняем только поле avatar
            logger.info(f"Аватар создан для пользователя {instance.email}")
        except Exception as e:
            logger.error(f"Не удалось создать аватар для {instance.email}: {e}")
