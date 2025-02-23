from django.core.management.base import BaseCommand
from ads.models import Category  # Убедись, что у тебя есть модель Category!

class Command(BaseCommand):
    help = "Создаёт категории по умолчанию"

    def handle(self, *args, **kwargs):
        categories = ["Тварини", "Автомобілі", "Мотоцикли", "Скутери", "Мебель", 
    "Антикваріат", "Ножі", "Робота", "Нерухомість", "Запчастини",
    "Дім і сад", "Електроніка", "Бізнес", "Хобі", "Одяг", "Інше"]
        for name in categories:
            Category.objects.get_or_create(name=name)
        self.stdout.write(self.style.SUCCESS("Категории успешно добавлены!"))