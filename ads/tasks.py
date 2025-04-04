from celery import shared_task
from datetime import timedelta
from django.utils import timezone
from ads.models import Ad

@shared_task
def remove_expired_ads():
    # Получаем текущее время
    now = timezone.now()

    # Удаляем стандартные объявления, которые не обновлялись в течение недели
    Ad.objects.filter(is_standard=True, created_at__lte=now - timedelta(weeks=1)).delete()

    # Удаляем популярные объявления, которые не обновлялись в течение 20 дней
    Ad.objects.filter(is_popular=True, created_at__lte=now - timedelta(days=20)).delete()

    # Удаляем премиум объявления, которые не обновлялись в течение месяца
    Ad.objects.filter(is_premium=True, premium_until__lte=now).delete()

    return 'Expired ads removed successfully'
