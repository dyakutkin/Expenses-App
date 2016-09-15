import django_filters
from rest_framework import filters

from expenses.models import Expense


class ExpenseFilter(filters.FilterSet):
    date_from = django_filters.DateFilter(name="date", lookup_expr='gte')
    date_to = django_filters.DateFilter(name="date", lookup_expr='lte')
    time_from = django_filters.TimeFilter(name="time", lookup_expr='gte')
    time_to = django_filters.TimeFilter(name="time", lookup_expr='lte')

    class Meta:
        model = Expense