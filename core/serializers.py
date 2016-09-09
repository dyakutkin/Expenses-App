from django.contrib.auth.models import User
from rest_framework import serializers

from core.models import Item


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User


class ItemFilterSerializer(serializers.Serializer):
    date_from = serializers.DateField(required=False)
    date_to = serializers.DateField(required=False)
    time_from = serializers.TimeField(required=False)
    time_to = serializers.TimeField(required=False)
