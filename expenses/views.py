from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import HttpResponse
from django.db.models import Q
from django.views.decorators.csrf import ensure_csrf_cookie

from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView

from expenses.permissions import PermittedExpensesQuerysetMixin, UserManagementPermission

from expenses.models import Expense
from expenses.serializers import (ExpenseSerializer, ExpenseFilterSerializer, UserSerializer)


class FilteringViewMixin(object):
    def get(self, request):
        filter_serializer = self.filter_serializer_class(data=request.GET)
        filter_serializer.is_valid(raise_exception=True)
        filters = Q()

        for k, v in self.filter_args_mapping.items():
            arg = filter_serializer.validated_data.get(k)
            if arg:
                filters &= Q(**{v: arg})

        queryset = self.model_class.objects.filter(filters)
        data_serializer = self.data_serializer_class(queryset, many=True)
        return Response(data=data_serializer.data)


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


class ExpensesView(PermittedExpensesQuerysetMixin, ModelViewSet):
    serializer_class = ExpenseSerializer

    def create(self, serializer):
        data = self.request.data.copy()
        data['user'] = self.request.user.id
        serializer = self.serializer_class(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return HttpResponse(status=400)


class FilteredExpensesView(PermittedExpensesQuerysetMixin, FilteringViewMixin, APIView):
    filter_args_mapping = {
        'date_from': 'date__gte',
        'date_to': 'date__lte',
        'time_from': 'time__gte',
        'time_to': 'time__lte',
    }
    filter_serializer_class = ExpenseFilterSerializer
    data_serializer_class = ExpenseSerializer
    model_class = Expense
