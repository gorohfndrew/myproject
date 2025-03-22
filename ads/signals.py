from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import Profile
from .models import Profile, CustomUser

# Сигнал для создания профиля при создании пользователя
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_or_update_profile(sender, instance, created, **kwargs):
    # Если пользователь только что был создан, создаем профиль
    if created:
        Profile.objects.create(user=instance, phone_number=instance.phone_number)
    else:
        # Если профиль уже существует, обновляем его
        if hasattr(instance, 'profile'):
            instance.profile.phone_number = instance.phone_number  # Обновляем номер телефона
            instance.profile.save()

# Сигнал для сохранения профиля при изменении пользователя
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_user_profile(sender, instance, **kwargs):
    # Проверка, если профиль существует, сохраняем его
    if hasattr(instance, 'profile'):
        instance.profile.save()

