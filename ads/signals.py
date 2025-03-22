from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import Profile

# Сигнал для создания профиля при создании пользователя
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        # Создание профиля для нового пользователя
        Profile.objects.create(user=instance)

# Сигнал для сохранения профиля при изменении пользователя
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_user_profile(sender, instance, **kwargs):
    # Проверка, если профиль существует, сохраняем его
    if hasattr(instance, 'profile'):
        instance.profile.save()