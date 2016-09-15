from django.contrib.auth.models import User
from rest_framework import serializers

from expenses.models import Expense


class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
