from django.shortcuts import render
from rest_framework import viewsets
from .models import Ad, Category
from .serializers import AdSerializer, CategorySerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class AdViewSet(viewsets.ModelViewSet):
    queryset = Ad.objects.all()
    serializer_class = AdSerializer
# Create your views here.
