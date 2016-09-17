from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie

from rest_framework import filters
from rest_framework.viewsets import ModelViewSet

from expenses.permissions import UserManagementPermission, ExpensesPermission
from expenses.models import Expense
from expenses.serializers import (ExpenseSerializer, UserSerializer)
from expenses.filters import ExpenseFilter


@ensure_csrf_cookie
def login_view(request):
    if not request.user.is_authenticated:
        user = authenticate(
            username=request.POST.get('username'),
            password=request.POST.get('password'))
        if user:
            login(request, user)
            return JsonResponse(UserSerializer(request.user).data)
        return HttpResponse(status=401)
    return JsonResponse(UserSerializer(request.user).data)


class UsersView(ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [UserManagementPermission]


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
