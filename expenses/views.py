from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import HttpResponse
from django.views.decorators.csrf import ensure_csrf_cookie

from rest_framework import status, filters
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from expenses.permissions import UserManagementPermission
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
            return HttpResponse(status=200)
        return HttpResponse(status=401)
    return HttpResponse(status=200)


class UsersView(ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [UserManagementPermission]


class ExpensesView(ModelViewSet):
    serializer_class = ExpenseSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = ExpenseFilter

    def get_queryset(self):
        queryset = Expense.objects.filter(user=self.request.user)
        if self.request.user.groups.filter(name='admin').exists():
            queryset = Expense.objects.all()
        elif self.request.user.groups.filter(name='user_manager').exists():
            queryset = None
        return queryset

    def create(self, serializer):
        data = self.request.data.copy()
        data['user'] = self.request.user.id
        serializer = self.serializer_class(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return HttpResponse(status=400)
