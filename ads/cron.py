from django.utils import timezone
from ads.models import Ad
def update_ad_status():
    now = timezone.now()
    ads = Ad.objects.all()
    for ad in ads:
        # Обновление статуса по дате окончания публикации
        if ad.publication_end_date < now:
            ad.is_active = False
        
        # Обновление статуса по дням в ТОПе
        if ad.top_days <= 0:
            ad.is_in_top = False
        
        # Обновление статуса по доступным поднятиям
        if ad.available_boosts <= 0:
            ad.can_boost = False
        
        ad.save()