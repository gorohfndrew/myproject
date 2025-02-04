# mydona/serializers.py
from rest_framework import serializers
from .templates.ads.models import Ad, Category

class AdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ad
        fields = '__all__'  # This includes all the fields from the Ad model

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'  # This includes all the fields from the Category model