from django.contrib.auth.models import User
from rest_framework import serializers

from expenses.models import Expense


class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense


class ExpenseFilterSerializer(serializers.Serializer):
    date_from = serializers.DateField(required=False)
    date_to = serializers.DateField(required=False)
    time_from = serializers.TimeField(required=False)
    time_to = serializers.TimeField(required=False)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
