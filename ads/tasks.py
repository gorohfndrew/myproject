# myapp/tasks.py
from celery import shared_task
from django.utils import timezone
from ads.models import Ad

@shared_task
def update_ad_status():
    now = timezone.now()
    ads = Ad.objects.all()
    for ad in ads:
        # Логика обновления статуса
        if ad.publication_end_date < now:
            ad.is_active = False
        
        if ad.top_days <= 0:
            ad.is_in_top = False
        
        if ad.available_boosts <= 0:
            ad.can_boost = False
        
        ad.save()