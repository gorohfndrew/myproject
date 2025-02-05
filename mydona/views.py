from django.shortcuts import render
from .models import Ad
from django.views import View

def ads_list(request):
    ads = Ad.objects.all()
    return render(request, 'ads/index.html', {'ads': ads})
class RegisterView(View):
    def get(self, request):
        return render(request, 'ads/register.html')  # Убедитесь, что путь правильный
# Create your views here.
