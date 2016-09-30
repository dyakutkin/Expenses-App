from django.contrib.auth.models import User, Group

from rest_framework import filters
from rest_framework.viewsets import ModelViewSet
from rest_framework.exceptions import NotAcceptable

from expenses.permissions import UserManagementPermission, ExpensesPermission
from expenses.models import Expense
from expenses.serializers import (ExpenseSerializer, UserSerializer)
from expenses.filters import ExpenseFilter


class UsersView(ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [UserManagementPermission]

    def get_queryset(self):
        if self.request.user.groups.filter(name='user_manager').exists():
            return Group.objects.get(name='user').user_set.all()
        return User.objects.all()

    def perform_create(self, serializer):
        instance = serializer.save()
        instance.groups.add(Group.objects.get(name='user'))


class ExpensesView(ModelViewSet):
    serializer_class = ExpenseSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = ExpenseFilter
    permission_classes = [ExpensesPermission]

    def get_queryset(self):
        if self.request.user.groups.filter(name='admin').exists():
            queryset = Expense.objects.all()
        else:
            queryset = Expense.objects.filter(user=self.request.user)
        return queryset

    def create(self, request, *args, **kwargs):
        if request.user.groups.filter(name='user').exists() \
                and int(request.data.get('user', -1)) != request.user.id:
            raise NotAcceptable("You don't have rights to create expenses for other users.")
        return super(ExpensesView, self).create(request, *args, **kwargs)
